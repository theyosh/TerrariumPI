#!/bin/bash

# Some settings
RUN_AS_USER="pi"
SCREEN_NAME="TerrariumPI"
RESTART_TIME=10
MAX_RESTARTS=5
RESTART_TIMEOUT=45
PYTHON=2
PYTHON_VERSION=$1
if [ "${PYTHON_VERSION}" == "3" ]; then
  PYTHON=3
fi
# End settings

# Main program
RESTART_ATTEMPTS=0
BASEDIR=$(dirname $(readlink -nf $0))
SCRIPT=$(basename $(readlink -nf $0))
RUN=$2
IP=`ip -4 addr | grep inet | grep -v "127.0.0.1" | grep -o -P "inet \K([0-9.]+)" | head -n1`
# Overrule default user based on the installation directory user rights
RUN_AS_USER=`stat -c "%U" "${BASEDIR}"`

function message {
  echo "$(date +"%Y-%m-%d %T,000") - INFO    - terrariumWrapper     - $1"
}

function update_software {
  # Initial run, no settings file, always up to date
  if [ -f "${BASEDIR}/settings.cfg" ]; then

    # Read out the new and current versions
    NEW_VERSION=`grep ^version "${BASEDIR}/settings.cfg" | cut -d' ' -f 3 | sed "s/\.//g"`
    CURRENT_VERSION=`grep ^version "${BASEDIR}/settings.cfg" | cut -d' ' -f 3 | sed "s/\.//g"`

    # New version detected? Return true for updating
    if [ "${CURRENT_VERSION}" -lt "${NEW_VERSION}" ]; then
      return 0
    else
      # No update, return false
      return 1
    fi
  fi

  # Return false
  return 1
}

if [ "${RUN}" == "run" ]
then
  while true
  do
    # Reset internal bash seconds counter
    SECONDS=0

    # Start terrarium software
    message "Starting TerrariumPI server at location: http://${IP}:8090 ..."
    if [ $PYTHON -eq 2 ]; then
      python "${BASEDIR}/terrariumPI.py"
    elif [ $PYTHON -eq 3 ]; then
      python3 "${BASEDIR}/terrariumPI.py"
    fi

    # Check after run if there is an update. If so, show message and exit
    if update_software ; then
      message "A new version of TerrariumPI is detected. Please restart."
      sleep 5
      break
    fi

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
    echo "Start TerrariumPI as user root"
    echo "sudo ./start.sh"
    exit 0
  fi

  # Update version?
  if update_software ; then
    message "TerrariumPI has detected an update and will now run the installer to update all dependencies and libraries."
    ./install.sh ${PYTHON}

    message "Updating TerrariumPI software is done and will now start in 5 seconds. Press Ctrl+C to abort."
    for (( counter=5; counter>0; counter-- ))
    do
      echo -n "${counter} "
      sleep 1
    done
  fi

  message "Starting TerrariumPI server running as user '${RUN_AS_USER}' at location: http://${IP}:8090 ..."
  cd "${BASEDIR}"

  su ${RUN_AS_USER} -c "screen -dmS ${SCREEN_NAME} ./${SCRIPT} ${PYTHON} run"
fi
