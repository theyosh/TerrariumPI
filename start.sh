#!/bin/bash

RUN_AS_USER="pi"
SCREEN_NAME="gekko"
RESTART_TIME=15
BASEDIR=$(dirname $(readlink -f $0))
RUN=$1


if [ "${RUN}" == "run" ]
then
  RESTART_ATTEMPTS=0
  SECONDS=0
  while true
  do
    ${BASEDIR}/terrarium.py

#    if test $SECONDS le 30
#    then
#      RESTART_ATTEMPTS=$((RESTART_ATTEMPTS+1))
#    fi

#    if test $RESTART_ATTEMPTS gt 10
#    then
#      echo "To manny errors, reboting"
#      sync
#      reboot
#    fi

    echo -n "Restarting in ${RESTART_TIME} seconds after ${SECONDS} seconds of running"
    for (( counter=1; counter<=${RESTART_TIME}; counter++ ))
    do
      echo -n "."
      sleep 1
    done
    echo ""
  done
else
  echo "Starting terrarium server software... ${BASEDIR}"
  cd "${BASEDIR}"
  screen -dmS ${SCREEN_NAME} su ${RUN_AS_USER} -c "./start.sh run"
fi
