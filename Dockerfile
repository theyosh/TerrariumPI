# Build for raspberry pi
# docker buildx build --platform linux/arm/v7 --progress=plain -t theyosh/terrariumpi:4.0.0 -f Dockerfile --push .

# build sispmctl 4.9
FROM gcc:9.4.0-buster as sispmctl_builder
ENV SISPMCTL_VERSION="4.9"
WORKDIR /sispmctl
RUN apt-get update && apt-get install -y --no-install-recommends libusb-dev && \
  wget https://sourceforge.net/projects/sispmctl/files/sispmctl/sispmctl-${SISPMCTL_VERSION}/sispmctl-${SISPMCTL_VERSION}.tar.gz/download -O sispmctl-${SISPMCTL_VERSION}.tar.gz && \
  tar zxvf sispmctl-${SISPMCTL_VERSION}.tar.gz && \
  cd sispmctl-${SISPMCTL_VERSION}/ && \
  ./configure && \
  make && \
  make install

# python builder, help keep image small
FROM python:3.8-buster as python_builder
ARG GITHUB_SHA=${GITHUB_SHA}

ENV DEBIAN_FRONTEND=noninteractive
# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
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
RUN pip install --upgrade pip==22.2.2 && pip install wheel==0.37.1
COPY requirements.txt .
# requirements are slightly different for docker
RUN sed -i 's/opencv-python-headless/# opencv-python-headless/g' requirements.txt && \
  sed -i 's/cryptography==.*/cryptography==3.4.8/g' requirements.txt && \
  sed -i 's/numpy==.*/numpy==1.21.4/g' requirements.txt && \
  pip install -r requirements.txt && \
  find /opt/venv -type d -name  "__pycache__" -exec rm -r {} +

WORKDIR /TerrariumPI
# Set git version in a temp file
RUN echo "${GITHUB_SHA}" > .gitversion
# Just clone the libraries, ignore docker cache...
RUN git clone https://github.com/SequentMicrosystems/4relay-rpi.git --depth 1 "3rdparty/4relay-rpi" && \
  git clone https://github.com/PiSupply/Bright-Pi.git --depth 1 "3rdparty/Bright-Pi" && \
  git clone https://github.com/ageir/chirp-rpi.git --depth 1 "3rdparty/chirp-rpi" && \
  git clone https://github.com/perryflynn/energenie-connect0r.git --depth 1 "3rdparty/energenie-connect0r" && \
  git clone https://github.com/SequentMicrosystems/relay8-rpi.git --depth 1 "3rdparty/relay8-rpi" && \
  git clone https://github.com/SequentMicrosystems/4relind-rpi.git --depth 1 "3rdparty/4relind-rpi" && \
  git clone https://github.com/SequentMicrosystems/8relind-rpi.git --depth 1 "3rdparty/8relind-rpi" && \
  git clone https://github.com/AtlasScientific/Raspberry-Pi-sample-code.git --depth 1 "3rdparty/AtlasScientific" && \
  git clone https://github.com/fancyapps/fancybox.git --depth 1 "static/assets/plugins/fancybox" && \
  git clone https://github.com/mapshakers/leaflet-icon-pulse.git --depth 1 "static/assets/plugins/leaflet.icon-pulse" && \
  git clone https://github.com/ebrelsford/Leaflet.loading.git --depth 1 "static/assets/plugins/leaflet.loading" && \
  rm -Rf 3rdparty/Bright-Pi/Documents && \
  find . -type d -name ".git" -exec rm -r {} +


FROM python:3.8-buster as sourcecode
WORKDIR /TerrariumPI
COPY . .
# remove git and 3rdparty dir from code copy to help keep image smaller
# 3rdparty is coming from the builder image
RUN rm -Rf .git 3rdparty
# Compress JS and CSS files so browsers can download compressed versions of the files
RUN find static/assets/ -type f -regex ".*\.\(css\|js\)" -exec gzip -f9k '{}' \;

# actual image
FROM python:3.8-slim-buster as finalimage
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
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
  apt-get --purge autoremove -y && rm -rf /var/lib/apt/lists/*
COPY --from=sispmctl_builder /usr/local/lib/libsispmctl* /usr/local/lib/.
COPY --from=sispmctl_builder /usr/local/bin/sispmctl /usr/local/bin/sispmctl
RUN rm /usr/local/lib/libsispmctl.so /usr/local/lib/libsispmctl.so.0 && ln -s /usr/local/lib/libsispmctl.so.0.2.1 /usr/local/lib/libsispmctl.so && ln -s /usr/local/lib/libsispmctl.so.0.2.1 /usr/local/lib/libsispmctl.so.0 && \
  ldconfig
ENV PATH="/opt/venv/bin:$PATH"
COPY --from=python_builder /opt/venv /opt/venv
RUN ln -s /usr/lib/python3/dist-packages/cv2.cpython-37m-arm-linux-gnueabihf.so /opt/venv/lib/python3.8/site-packages/cv2.so && \
  mv /usr/lib/python3.7/gettext.py /usr/local/lib/python3.8/gettext.py && \
  rm -rf /usr/lib/python3/dist-packages/numpy /usr/lib/python3/dist-packages/numpy-1.16.2.egg-info
RUN echo "/opt/vc/lib" > /etc/ld.so.conf.d/00-vmcs.conf
WORKDIR /TerrariumPI
COPY --from=python_builder /TerrariumPI/ /TerrariumPI/.
COPY --from=sourcecode /TerrariumPI /TerrariumPI
RUN echo '[ ! -z "$TERM" -a -r /TerrariumPI/motd.sh ] && /TerrariumPI/motd.sh' >> /etc/bash.bashrc

HEALTHCHECK --interval=180s --timeout=5s --start-period=120s CMD python contrib/docker_health.py

ENTRYPOINT ["/bin/bash", "/TerrariumPI/run.sh"]
