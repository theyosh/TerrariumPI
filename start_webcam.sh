#!/bin/bash

RUN_AS_USER="pi"
SCREEN_NAME="rpicam"
RESTART_TIME=15
BASEDIR=$(dirname $(readlink -f $0))
START_SCRIPT=$(basename "$0")
RUN=$1

if [ "${RUN}" == "run" ]
then
  BASEDIR="${BASEDIR}/mjpg-streamer-experimental"
  while true
  do
    export LD_LIBRARY_PATH=${BASEDIR}
    ${BASEDIR}/mjpg_streamer \
        -i "input_uvc.so -d /dev/video0 -r 1280x720 -led 0" \
        -i "input_raspicam.so -x 1920 -y 1080 -fps 15 -ex auto -awb auto -vs" \
        -o "output_http.so -w ${PWD}/www -p 8080"

    echo "Restarting in ${RESTART_TIME} seconds"
    sleep ${RESTART_TIME}
  done
else
  echo "Starting rpi-cam software... ${BASEDIR}"
  cd "${BASEDIR}"
  screen -dmS ${SCREEN_NAME} su ${RUN_AS_USER} -c "./${START_SCRIPT} run"
fi
