# Build for raspberry pi
# docker buildx build --platform linux/arm/v7 --progress=plain -t theyosh/terrariumpi:4.0.0 -f Dockerfile --push .

# build sispmctl 4.9
FROM gcc:9.4.0-buster as sispmctl_builder
RUN apt-get update && apt-get install -y --no-install-recommends libusb-dev && \
  wget https://sourceforge.net/projects/sispmctl/files/sispmctl/sispmctl-4.9/sispmctl-4.9.tar.gz/download -O sispmctl-4.9.tar.gz && \
  tar zxvf sispmctl-4.9.tar.gz && \
  cd sispmctl-4.9/ && \
  ./configure && \
  make && \
  make install

# python builder, help keep image small
FROM python:3.8-buster as builder
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends gnupg ca-certificates && \
  echo "deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi" > /etc/apt/sources.list.d/raspberrypi.list && \
  echo "deb http://archive.raspberrypi.org/debian/ buster main" >> /etc/apt/sources.list.d/raspberrypi.list && \
  echo "deb [arch=armhf] https://download.docker.com/linux/raspbian buster stable" > /etc/apt/sources.list.d/docker.list && \
  apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9165938D90FDDD2E 82B129927FA3303E 7EA0A9C3F273FCD8 && \
  rm -rf /var/lib/apt/lists/* && \
  apt-get update && \
  apt-get install -y --no-install-recommends git libxslt1.1 libglib2.0-dev && \
  apt-get install -y --no-install-recommends python3-opencv libftdi1 libasound-dev
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# rpi.gpio - https://askubuntu.com/questions/1290037/error-while-installing-rpi-gpio-as-error-command-errored-out-with-exit-status
ENV CFLAGS=-fcommon
# cryptography - https://stackoverflow.com/questions/66118337/how-to-get-rid-of-cryptography-build-error
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN pip install --upgrade pip && pip install wheel
COPY requirements.txt .
# requirements are slightly different for docker
RUN sed -i 's/cryptography/cryptography==3.4.6/g' requirements.txt && \
  sed -i 's/opencv-python-headless/# opencv-python-headless/g' requirements.txt && \
  echo "numpy" >> requirements.txt && \
  pip install -r requirements.txt
WORKDIR /TerrariumPI
# we previously copied .git and then did git submodule init and submodule update, however as .git dir changes all the time it invalidates docker cache
RUN mkdir 3rdparty && cd 3rdparty && \
  git clone https://github.com/SequentMicrosystems/4relay-rpi.git && git -C "4relay-rpi" checkout "09a44bfbde18791750534ba204e1dfc7506a7eb2" && rm -rf "4relay-rpi/.git" && \
  git clone https://github.com/PiSupply/Bright-Pi.git && git -C "Bright-Pi" checkout "eccfbbb1221c4966cd337126bedcbb8bb03c3c71" && rm -rf "Bright-Pi/.git" && \
  git clone https://github.com/ageir/chirp-rpi.git && git -C "chirp-rpi" checkout "6e411d6c382d5e43ee1fd269ec4de6a316893407" && rm -rf "chirp-rpi/.git" && \
  git clone https://github.com/perryflynn/energenie-connect0r.git && git -C "energenie-connect0r" checkout "12ca24ab9d60cf4ede331de9a6817c3d64227ea0" && rm -rf "energenie-connect0r/.git" && \
  git clone https://github.com/SequentMicrosystems/relay8-rpi.git && git -C "relay8-rpi" checkout "5083730e415ee91fa4785e228f02a36e8bbaa717" && rm -rf "relay8-rpi/.git"
RUN mkdir -p static/assets/plugins && cd static/assets/plugins && \
  git clone https://github.com/fancyapps/fancybox.git "fancybox" && git -C "fancybox" checkout "eea1345256ded510ed9fae1e415aec2a7bb9620d" && rm -rf "fancybox/.git" && \
  git clone https://github.com/mapshakers/leaflet-icon-pulse.git "leaflet.icon-pulse" && git -C "leaflet.icon-pulse" checkout "f57da1e45f6d00f340f429a75a39324cad141061" && rm -rf "leaflet.icon-pulse/.git" && \
  git clone https://github.com/ebrelsford/Leaflet.loading.git "leaflet.loading" && git -C "leaflet.loading" checkout "7b22aff19a5a8fa9534fb2dcd48e06c6dc84b2ed" && rm -rf "leaflet.loading/.git"

# remove git and 3rdparty dir from code copy to help keep image smaller
# 3rdparty is coming from the builder image
FROM bash as sourcecode
WORKDIR /TerrariumPI
COPY . .
RUN rm -rf .git 3rdparty

# actual image
FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends gnupg ca-certificates && \
  echo "deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi" > /etc/apt/sources.list.d/raspberrypi.list && \
  echo "deb http://archive.raspberrypi.org/debian/ buster main" >> /etc/apt/sources.list.d/raspberrypi.list && \
  echo "deb [arch=armhf] https://download.docker.com/linux/raspbian buster stable" > /etc/apt/sources.list.d/docker.list && \
  apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9165938D90FDDD2E 82B129927FA3303E 7EA0A9C3F273FCD8 && \
  rm -rf /var/lib/apt/lists/* && \
  apt-get update && \
  apt-get install -y --no-install-recommends sudo pigpio ffmpeg libxslt1.1 && \
  apt-get install -y --no-install-recommends python3-opencv libftdi1 && \
  mkdir -p /usr/share/man/man1 && apt-get install -y --no-install-recommends openjdk-11-jre-headless && \
  apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
COPY --from=sispmctl_builder /usr/local/lib/libsispmctl* /usr/local/lib/.
COPY --from=sispmctl_builder /usr/local/bin/sispmctl /usr/local/bin/sispmctl
RUN rm /usr/local/lib/libsispmctl.so /usr/local/lib/libsispmctl.so.0 && ln -s /usr/local/lib/libsispmctl.so.0.2.1 /usr/local/lib/libsispmctl.so && ln -s /usr/local/lib/libsispmctl.so.0.2.1 /usr/local/lib/libsispmctl.so.0 && \
  ldconfig
ENV PATH="/opt/venv/bin:$PATH"
COPY --from=builder /opt/venv /opt/venv
RUN ln -s /usr/lib/python3/dist-packages/cv2.cpython-37m-arm-linux-gnueabihf.so /opt/venv/lib/python3.8/site-packages/cv2.so && \
  mv /usr/lib/python3.7/gettext.py /usr/local/lib/python3.8/gettext.py && \
  rm -rf /usr/lib/python3/dist-packages/numpy /usr/lib/python3/dist-packages/numpy-1.16.2.egg-info
WORKDIR /TerrariumPI
COPY --from=builder /TerrariumPI/ /TerrariumPI/.
COPY --from=sourcecode /TerrariumPI /TerrariumPI

HEALTHCHECK --interval=120s --timeout=5s --start-period=120s CMD python contrib/docker_health.py

ENTRYPOINT ["/bin/bash", "/TerrariumPI/run.sh"]
