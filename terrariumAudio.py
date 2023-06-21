# -*- coding: utf-8 -*-
import terrariumLogging

logger = terrariumLogging.logging.getLogger(__name__)

from gevent import sleep
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
                (_, longname) = alsaaudio.card_name(i)
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
            value = max(0, min(120, 120 * (value / 100)))
            mixer.setvolume(int(value), alsaaudio.MIXER_CHANNEL_ALL)


class terrariumAudioPlayer(object):
    CMD = "/usr/bin/ffmpeg"

    def __init__(self, hw, playlists=[], shuffle=False, repeat=False):
        self.__hw = hw
        self.__stop = False
        self.__player = {"ffmpeg": None, "thread": None, "exit_status": None}

        self.playlists = playlists
        self.shuffle = shuffle
        self.repeat = repeat

    def __run(self):
        self.__stop = False
        for playlist in self.playlists:
            if self.__stop:
                break

            files = copy.copy(playlist["files"])

            if playlist.get("shuffle"):
                random.shuffle(files)

            self.volume(playlist.get("volume", 80))

            repeat = playlist.get("repeat", False)
            first_start = True
            while not self.__stop and (repeat or first_start):
                first_start = False

                playlist = [f"file '{audiofile}'" for audiofile in files]

                with tempfile.NamedTemporaryFile() as fp:
                    fp.write("\n".join(playlist).encode())
                    fp.flush()

                    cmd = f"{self.CMD} -hide_banner -nostdin -v 0 -f concat -safe 0 -i {fp.name} -f alsa hw:{self.__hw}".split(
                        " "
                    )
                    self.__player["ffmpeg"] = psutil.Popen(cmd, stdout=DEVNULL)
                    self.__player["exit_status"] = self.__player["ffmpeg"].poll()
                    while self.__player["exit_status"] is None:
                        self.__player["exit_status"] = self.__player["ffmpeg"].poll()
                        sleep(1)

        self.__player["ffmpeg"] = None

    def play(self):
        if self.running:
            self.stop()

        if len(self.playlists) > 0:
            self.__player["thread"] = threading.Thread(target=self.__run)
            self.__player["thread"].start()

    def stop(self):
        self.__stop = True
        if self.running:
            self.__player["ffmpeg"].terminate()
            self.__player["thread"].join()

    @property
    def playlists(self):
        return self.__playlists

    @playlists.setter
    def playlists(self, playlists):
        self.__playlists = copy.copy(playlists)

    @property
    def running(self):
        return self.__player["ffmpeg"] is not None and self.__player["ffmpeg"].poll() is None

    def volume(self, value):
        terrariumAudio.volume(int(self.__hw), int(value))
