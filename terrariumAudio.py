# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from time import sleep
import psutil
from subprocess import DEVNULL
import threading
import copy

import alsaaudio
import tempfile
import random

from terrariumUtils import classproperty


class terrariumAudio(object):
    @classproperty
    def available_soundcards(__cls__):
        soundcards = []
        for i in alsaaudio.card_indexes():
            try:
                _, longname = alsaaudio.card_name(i)
                soundcards.append({"index": int(i), "name": longname})

            except Exception as ex:
                # Just ignore error, and skip it
                logger.debug(f"Not a valid soundcard. Just ignore: {ex}")

        return soundcards

    @classmethod
    def volume(__cls__, hw, value=None):
        try:
            mixer = alsaaudio.Mixer(control="PCM", cardindex=hw)
        except alsaaudio.ALSAAudioError as ex:
            logger.debug(f"Falling back to headphones: {ex}")
            try:
                mixer = alsaaudio.Mixer(control="Headphone", cardindex=hw)
            except alsaaudio.ALSAAudioError as ex:
                logger.error(
                    f'Hardware \'{terrariumAudio.available_soundcards[hw]["name"]}\' is not correct, so we cannot set the player audio volume.: {ex}'
                )
                return None

        if value is None:
            # We get stereo volume but asume that left and right channel are at the same volume.
            return mixer.getvolume()[0]

        else:
            try:
                # Try to 'overload' the volume by 20%. Can work for some sound cards
                value = int(max(0, min(120, 120 * (value / 100))))
                mixer.setvolume(value, alsaaudio.MIXER_CHANNEL_ALL)
            except alsaaudio.ALSAAudioError:
                try:
                    # When the 'overloaded' value is to high, fall back to normal max volume
                    value = int(max(0, min(100, value)))
                    mixer.setvolume(value, alsaaudio.MIXER_CHANNEL_ALL)
                except alsaaudio.ALSAAudioError as ex:
                    logger.error(
                        f'Error setting sound card \'{terrariumAudio.available_soundcards[hw]["name"]}\' to volume {value} : {ex}'
                    )


class terrariumAudioPlayer(object):
    CMD = "/usr/bin/ffmpeg"

    def __init__(self, hw, playlists=[], shuffle: bool = False, repeat: bool = False) -> None:
        self.__hw = hw
        self.__player = {"ffmpeg": None, "thread": None, "exit_status": None}
        self.__stopping = False
        self.__running = False

        self.playlists = playlists
        self.shuffle = shuffle
        self.repeat = repeat
        self.audio_volume = 0

    def __run(self) -> None:
        for playlist in self.playlists:
            files = copy.copy(playlist.get("files", []))

            if len(files) == 0:
                break

            self.shuffle = playlist.get("shuffle", False)
            self.repeat = playlist.get("repeat", False)
            self.audio_volume = playlist.get("volume", 80)

            if self.shuffle:
                random.shuffle(files)

            self.volume(self.audio_volume)
            first_start = True

            logger.info(
                f"Start playing {'shuffled ' if self.shuffle else ' '}{len(files)} audio files in {'repeat' if self.repeat else 'normal'} mode at volume {self.audio_volume}"
            )
            while not self.__stopping and (first_start or self.repeat):
                first_start = False

                playlist = [f"file '{audiofile}'" for audiofile in files]

                with tempfile.NamedTemporaryFile() as fp:
                    fp.write("\n".join(playlist).encode())
                    fp.flush()

                    cmd = f"{self.CMD} -hide_banner -nostdin -v 0 -f concat -safe 0 -i {fp.name} -f alsa hw:{self.__hw}".split(
                        " "
                    )
                    self.__player["ffmpeg"] = psutil.Popen(cmd, stdout=DEVNULL)
                    self.__player["exit_status"] = None

                    while self.__player["exit_status"] is None:
                        sleep(1)
                        self.__player["exit_status"] = self.__player["ffmpeg"].poll()

                if not self.__stopping and self.__player["exit_status"] != None and self.__player["exit_status"] != 0:
                    # Player crashed or killed out-site TerrariumPI
                    self.__running = False

            if self.__stopping:
                break

        self.__player["ffmpeg"] = None

    def play(self) -> None:
        self.__stopping = False

        if self.running:
            self.stop()

        if len(self.playlists) == 0:
            logger.warning(f'No playlist(s) selected. Cannot start player.')
            return

        logger.info(f"Starting audio player with {len(self.__playlists)} playlist(s)")
        self.__player["thread"] = threading.Thread(target=self.__run)
        self.__player["thread"].start()

        self.__running = True

    def stop(self) -> None:
        self.__stopping = True

        if self.running:
            logger.info(f"Stopping audio player")
            if self.__player["ffmpeg"] is not None:
                self.__player["ffmpeg"].terminate()
                self.__player["thread"].join()

        self.__running = False

    @property
    def playlists(self):
        return self.__playlists

    @playlists.setter
    def playlists(self, playlists) -> None:
        self.__playlists = copy.copy(playlists)

    @property
    def running(self) -> bool:
        return self.__running

    def volume(self, value) -> None:
        terrariumAudio.volume(int(self.__hw), int(value))
