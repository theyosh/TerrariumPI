#!/bin/bash
# Cronjob to run every minute
# add using command 'crontab -e' as running TerrariumPI user
# * * * * * ~/TerrariumPI/watchdog.sh

BASEDIR=$(dirname $(readlink -nf $0))
RUN_AS_USER=`stat -c "%U" "${BASEDIR}"`
MAXTIME=600 # In seconds
LOGFILE="/home/${RUN_AS_USER}/TerrariumPI/log/terrariumpi.log"
PID="$(ps fax | grep terrariumPI.py | grep -v grep | awk {'print $1'})"
AGE="$(($(date +%s) - $(date +%s -r ${LOGFILE})))"

if [ $AGE -gt $MAXTIME ]; then
  echo "Logfile is not updated for $MAXTIME seconds. Restarting..."
  kill $PID
fi
