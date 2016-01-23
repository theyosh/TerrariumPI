#!/bin/bash

# Some settings
RUN_AS_USER="pi"
SCREEN_NAME="gekko"
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
  echo "$(date +"%d-%m-%Y %T"): $1"
}

if [ "${RUN}" == "run" ]
then
  while true
  do
    # Reset internal bash seconds counter
    SECONDS=0

    # Start terrarium software
    message "Starting terrarium server software..."
    ${BASEDIR}/terrarium.py

    # Crashed / stopped / something else...
    if (( SECONDS < RESTART_TIMEOUT )); then
      # Restarted to soon... counting
      RESTART_ATTEMPTS=$((RESTART_ATTEMPTS+1))
      message "Restart counter: ${RESTART_ATTEMPTS}"

      if (( RESTART_ATTEMPTS > MAX_RESTARTS )); then
         # To many errors. Rebooting
         message "To manny error (${RESTART_ATTEMPTS}). Final result is reboting!!!"
         sync
         reboot
      fi

    else
      # Reset restart counter
      RESTART_ATTEMPTS=0
    fi

    echo -n "$(date +"%d-%m-%Y %T"): Restarting in ${RESTART_TIME} seconds after running for ${SECONDS} seconds "
    for (( counter=1; counter<=${RESTART_TIME}; counter++ ))
    do
      echo -n "."
      sleep 1
    done
    echo " restart!"
  done
else
  message "Starting terrarium server software..."
  cd "${BASEDIR}"
  screen -dmS ${SCREEN_NAME} su ${RUN_AS_USER} -c "./${SCRIPT} run"
fi
