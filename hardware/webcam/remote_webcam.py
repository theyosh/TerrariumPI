from . import terrariumWebcam
from terrariumUtils import terrariumUtils

from PIL import Image
from io import BytesIO


class terrariumRemoteWebcam(terrariumWebcam):
    HARDWARE = "remote"
    NAME = "Remote file webcam"
    VALID_SOURCE = r"^https?://.*(?<!\.m3u8)$"
    INFO_SOURCE = "http(s)://server.com/location/path/stream.jpg"

    def _load_hardware(self):
        remote_image = terrariumUtils.get_remote_data(self.address)
        if remote_image is not None:
            remote_image = Image.open(BytesIO(remote_image))
            # Update the resolution of the Webcam based on the remote source.
            # This will also update the resolution in the database when added.
            self.resolution = (remote_image.width, remote_image.height)
            return self.address

        return None

    def _get_raw_data(self):
        remote_image = terrariumUtils.get_remote_data(self.device)
        if remote_image is not None:
            return BytesIO(remote_image)

        return False
