
# Build for raspberry pi
# docker buildx build --platform linux/arm/v7 --progress=plain -t theyosh/terrariumpi:4.0.0 -f Dockerfile --push .

# python builder, help keep image small
FROM python:3.8.0 as builder
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y gnupg ca-certificates && \
  echo "deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi" > /etc/apt/sources.list.d/raspberrypi.list && \
  echo "deb http://archive.raspberrypi.org/debian/ buster main" >> /etc/apt/sources.list.d/raspberrypi.list && \
  echo "deb [arch=armhf] https://download.docker.com/linux/raspbian buster stable" > /etc/apt/sources.list.d/docker.list && \
  apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9165938D90FDDD2E 82B129927FA3303E 7EA0A9C3F273FCD8 && \
  rm -rf /var/lib/apt/lists/* && \
  apt-get update && \
  apt-get install -y --no-install-recommends bc screen git watchdog i2c-tools pigpio sqlite3 ffmpeg sispmctl ntp libxslt1.1 libglib2.0-dev && \
  apt-get install -y --no-install-recommends libopenexr23 libilmbase23 liblapack3 libatlas3-base && \
  apt-get install -y --no-install-recommends python3-opencv libftdi1 libasound-dev
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# picamera - https://github.com/waveform80/picamera/issues/578
ENV READTHEDOCS=True
# rpi.gpio - https://askubuntu.com/questions/1290037/error-while-installing-rpi-gpio-as-error-command-errored-out-with-exit-status
ENV CFLAGS=-fcommon
# cryptography - https://stackoverflow.com/questions/66118337/how-to-get-rid-of-cryptography-build-error
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN pip install --upgrade pip && pip install wheel
COPY requirements.txt .
# requirements are slightly different for docker
RUN sed -i 's/cryptography/cryptography==3.4.6/g' requirements.txt && \
  sed -i 's/opencv-python-headless/# opencv-python-headless/g' requirements.txt && \
  echo "numpy" >> requirements.txt && \
  pip install -r requirements.txt
WORKDIR /TerrariumPI
COPY .git .git
RUN git submodule init && \
  git submodule update && \
  rm -rf .git

# remove git dir from code copy to help keep image smaller
FROM python:3.8.0 as remove_git_dir
WORKDIR /TerrariumPI
COPY . .
RUN rm -rf .git

# actual image
FROM python:3.8.0-slim-buster
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends gnupg ca-certificates && \
  echo "deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi" > /etc/apt/sources.list.d/raspberrypi.list && \
  echo "deb http://archive.raspberrypi.org/debian/ buster main" >> /etc/apt/sources.list.d/raspberrypi.list && \
  echo "deb [arch=armhf] https://download.docker.com/linux/raspbian buster stable" > /etc/apt/sources.list.d/docker.list && \
  apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9165938D90FDDD2E 82B129927FA3303E 7EA0A9C3F273FCD8 && \
  rm -rf /var/lib/apt/lists/* && \
  apt-get update && \
  apt-get install -y --no-install-recommends bc screen git watchdog i2c-tools pigpio sqlite3 ffmpeg sispmctl ntp libxslt1.1 libglib2.0-dev && \
  apt-get install -y --no-install-recommends libopenexr23 libilmbase23 liblapack3 libatlas3-base && \
  apt-get install -y --no-install-recommends python3-opencv libftdi1 libasound-dev && \
  apt-get autoremove -y && rm -rf /var/lib/apt/lists/*
ENV PATH="/opt/venv/bin:$PATH"
COPY --from=builder /opt/venv /opt/venv
RUN ln -s /usr/lib/python3/dist-packages/cv2.cpython-37m-arm-linux-gnueabihf.so /opt/venv/lib/python3.8/site-packages/cv2.so && \
  mv /usr/lib/python3.7/gettext.py /usr/local/lib/python3.8/gettext.py && \
  rm -rf /usr/lib/python3/dist-packages/numpy /usr/lib/python3/dist-packages/numpy-1.16.2.egg-info
WORKDIR /TerrariumPI
COPY --from=builder /TerrariumPI/ /TerrariumPI/.
COPY --from=remove_git_dir /TerrariumPI /TerrariumPI
CMD ["/bin/bash", "/TerrariumPI/run.sh"]
