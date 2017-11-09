#!/bin/bash

# Some settings
RUN_AS_USER="pi"
SCREEN_NAME="TerrariumPI"
RESTART_TIME=10
MAX_RESTARTS=5
RESTART_TIMEOUT=45
# End settings

# Main program
RESTART_ATTEMPTS=0
BASEDIR=$(dirname $(readlink -nf $0))
SCRIPT=$(basename $(readlink -nf $0))
RUN=$1

function message {
  echo "$(date +"%Y-%m-%d %T,000") - INFO - terrariumWrapper - $1"
}

if [ "${RUN}" == "run" ]
then
  while true
  do
    # Reset soundcard???
    cvlc -q --no-interact silence.mp3 vlc://quit &
    # Reset internal bash seconds counter
    SECONDS=0

    # Start terrarium software
    message "Starting TerrariumPI server ..."
    python ${BASEDIR}/terrariumPI.py

    # Crashed / stopped / something else...
    if (( SECONDS < RESTART_TIMEOUT )); then
      # Restarted to soon... counting
      RESTART_ATTEMPTS=$((RESTART_ATTEMPTS+1))
      message "Restart counter: ${RESTART_ATTEMPTS}/${MAX_RESTARTS}"

      if (( RESTART_ATTEMPTS > MAX_RESTARTS )); then
         # To many errors. Rebooting
         message "To manny error (${RESTART_ATTEMPTS}). Shutting down TerrariumPI server!"
         exit 0
      fi

    else
      # Reset restart counter
      RESTART_ATTEMPTS=0
    fi

    message "Restarting in ${RESTART_TIME} seconds after running for ${SECONDS} seconds. Press Ctrl+C now to terminate TerrariumPI."
    for (( counter=${RESTART_TIME}; counter>0; counter-- ))
    do
      echo -n "${counter} "
      sleep 1
    done
    echo "restart!"

    # Restart PiGPIOd process....
    sudo service pigpiod restart
  done
else
  WHOAMI=`whoami`
  if [ "${WHOAMI}" != "root" ]; then
    message "Start TerrariumPI server as user root"
    exit 0
  fi

  message "Restarting TerrariumPI server running as user '${RUN_AS_USER}' ..."
  cd "${BASEDIR}"
  su ${RUN_AS_USER} -c "screen -dmS ${SCREEN_NAME} ./${SCRIPT} run"
fi
