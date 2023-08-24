# Build for raspberry pi
# docker buildx build --platform linux/arm/v7 --progress=plain -t theyosh/terrariumpi:4.0.0 -f Dockerfile --push .

# build sispmctl 4.9
FROM gcc:10-buster as sispmctl_builder
ARG SISPMCTL_VERSION="4.9"
WORKDIR /sispmctl
RUN apt-get update \
  && apt-get install -y --no-install-recommends libusb-dev \
  && wget https://sourceforge.net/projects/sispmctl/files/sispmctl/sispmctl-${SISPMCTL_VERSION}/sispmctl-${SISPMCTL_VERSION}.tar.gz/download -O sispmctl-${SISPMCTL_VERSION}.tar.gz \
  && tar zxvf sispmctl-${SISPMCTL_VERSION}.tar.gz --strip 1 \
  && ./configure \
  && make \
  && make install

# python builder, help keep image small
# Keep at 3.7-buster to use piwheels files for installation in stead of compiling them all manually. Saves about 2 hours of building :)
FROM python:3.7-buster as python_builder
# These two environment variables prevent __pycache__/ files.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/opt/venv/bin:$PATH"
RUN python -m venv /opt/venv
RUN pip install --upgrade pip==23.2.1 && pip install --upgrade wheel==0.41.2
COPY requirements.txt .
# requirements are slightly different for docker
RUN sed -i 's/numpy==.*/numpy==1.21.4/g' requirements.txt \
  && pip install -r requirements.txt --extra-index-url https://www.piwheels.org/simple \
  && find /opt/venv -type d -name  "__pycache__" -exec rm -r {} + \
  && find /opt/venv -type f -name "*.pyc" -delete \
  && find /opt/venv -type d -name ".git" -exec rm -r {} +

WORKDIR /TerrariumPI
# Just clone the libraries, ignore docker cache...
RUN git clone https://github.com/SequentMicrosystems/4relay-rpi.git --depth 1 "3rdparty/4relay-rpi" \
  && git clone https://github.com/PiSupply/Bright-Pi.git --depth 1 "3rdparty/Bright-Pi" \
  && git clone https://github.com/ageir/chirp-rpi.git --depth 1 "3rdparty/chirp-rpi" \
  && git clone https://github.com/perryflynn/energenie-connect0r.git --depth 1 "3rdparty/energenie-connect0r" \
  && git clone https://github.com/SequentMicrosystems/relay8-rpi.git --depth 1 "3rdparty/relay8-rpi" \
  && git clone https://github.com/SequentMicrosystems/4relind-rpi.git --depth 1 "3rdparty/4relind-rpi" \
  && git clone https://github.com/SequentMicrosystems/8relind-rpi.git --depth 1 "3rdparty/8relind-rpi" \
  && git clone https://github.com/AtlasScientific/Raspberry-Pi-sample-code.git --depth 1 "3rdparty/AtlasScientific" \
  && rm -Rf 3rdparty/Bright-Pi/Documents \
  && find . -type d -name  "__pycache__" -exec rm -r {} + \
  && find . -type f -name "*.pyc" -delete \
  && find . -type d -name ".git" -exec rm -r {} +

# Sourcecode cleanup and pre-prep
FROM python:3.7-buster as sourcecode
WORKDIR /TerrariumPI
COPY . .
# remove git and 3rdparty dir from code copy to help keep image smaller
# 3rdparty is coming from the builder image
RUN rm -Rf .git 3rdparty gui package*.json postcss.config.js rollup.config.js .env.* html-template.js requirements.txt yarn.lock

# actual image
FROM python:3.7-slim-buster as finalimage
ARG GITHUB_SHA
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/opt/venv/bin:$PATH"

RUN apt-get update \
  && apt-get install -y --no-install-recommends gnupg \
  && echo "deb http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi" > /etc/apt/sources.list.d/raspberrypi.list \
  && echo "deb http://archive.raspberrypi.org/debian/ buster main" >> /etc/apt/sources.list.d/raspberrypi.list \
  && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 9165938D90FDDD2E 82B129927FA3303E \
  && apt-get update \
  && apt-get full-upgrade -y --no-install-recommends \
  && apt-get install -y --no-install-recommends sudo pigpio ffmpeg libxslt1.1 libftdi1 libatlas3-base libgfortran5 libraspberrypi-bin openjdk-11-jre-headless \
  && apt-get --purge autoremove -y \
  && apt-get autoclean \
  && rm -rf /var/lib/apt/lists/* \
  && find /var/log/ -type f -delete \
  && find /var/cache/ -type f -delete

COPY --from=sispmctl_builder /usr/local/lib/libsispmctl* /usr/local/lib/.
COPY --from=sispmctl_builder /usr/local/bin/sispmctl /usr/local/bin/sispmctl

RUN rm /usr/local/lib/libsispmctl.so /usr/local/lib/libsispmctl.so.0 \
  && ln -s /usr/local/lib/libsispmctl.so.0.2.1 /usr/local/lib/libsispmctl.so \
  && ln -s /usr/local/lib/libsispmctl.so.0.2.1 /usr/local/lib/libsispmctl.so.0 \
  && echo "/opt/vc/lib" > /etc/ld.so.conf.d/00-vmcs.conf \
  && ldconfig

COPY --from=python_builder /opt/venv /opt/venv
COPY --from=python_builder /TerrariumPI/3rdparty /TerrariumPI/3rdparty
COPY --from=sourcecode /TerrariumPI /TerrariumPI

WORKDIR /TerrariumPI
# Set git version in a temp file
RUN echo "${GITHUB_SHA}" > .gitversion && echo '[ ! -z "$TERM" -a -r /TerrariumPI/motd.sh ] && /TerrariumPI/motd.sh' >> /etc/bash.bashrc

HEALTHCHECK --interval=180s --timeout=5s --start-period=120s CMD python contrib/docker_health.py

ENTRYPOINT ["/bin/bash", "/TerrariumPI/run.sh"]
