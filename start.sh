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
  echo "$(date +"%Y-%m-%d %T,000") - INFO    - terrariumWrapper - $1"
}

if [ "${RUN}" == "run" ]
then
  while true
  do
    # Reset internal bash seconds counter
    SECONDS=0

    # Start terrarium software
    message "Starting TerrariumPI server ..."
    python ${BASEDIR}/terrariumPI.py

    # Crashed / stopped / something else...
    if (( SECONDS < RESTART_TIMEOUT )); then
      # Restarted to soon... counting
      RESTART_ATTEMPTS=$((RESTART_ATTEMPTS+1))
      message "Restart counter: ${RESTART_ATTEMPTS}"

      if (( RESTART_ATTEMPTS > MAX_RESTARTS )); then
         # To many errors. Rebooting
         message "To manny error (${RESTART_ATTEMPTS}). Shutting down TerrariumPI server!"
         exit 0
      fi

    else
      # Reset restart counter
      RESTART_ATTEMPTS=0
    fi

    echo -n "$(date +"%Y-%m-%d %T,000") - WARNING - terrariumWrapper - Restarting in ${RESTART_TIME} seconds after running for ${SECONDS} seconds "
    for (( counter=1; counter<=${RESTART_TIME}; counter++ ))
    do
      echo -n "."
      sleep 1
    done
    echo " restart!"
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
