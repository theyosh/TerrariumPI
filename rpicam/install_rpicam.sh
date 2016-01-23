#!/bin/bash

# Basic config:
raspi-config

# Install extra softwre for MJPEG-Streamer
# Enable RPI cam with raspi-config tool
aptitude -y install libjpeg-dev cmake git

#RPI Cam streaming
HOMEDIR="/home/pi"
git clone https://github.com/jacksonliam/mjpg-streamer.git ${HOMEDIR}/rpicam
cp start_rpicam.sh ${HOMEDIR}/rpicam/
chmod +x ${HOMEDIR}/rpicam/start_rpicam.sh
cd ${HOMEDIR}/rpicam/mjpg-streamer-experimental/
make clean all
chown pi ${HOMEDIR}/rpicam/* -R

echo "Start rpi camera with ${HOMEDIR}/rpicam/start_rpicam.sh"
