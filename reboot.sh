#!/bin/bash

#exit 0

# Which Interface do you want to check
wlan='wlan0'
# Which address do you want to ping to see if you can connect
pingip='192.168.5.1'
# Logfile
log="/home/pi/terrarium/reboot.log"
# Minimal uptime in seconds
minuptime=120
# TMP File
tmpfile="/tmp/wifi.counter"

date=$(date +"[%d-%m-%Y %H:%M:%S]")
running=$(awk '{print int($1)}' /proc/uptime)

# Perform the network check and reset if necessary
/bin/ping -c 2 -I $wlan $pingip > /dev/null 2> /dev/null
if [ $? -ge 1 ] ; then
    if [ $running -gt $minuptime ]; then
        echo "$date Network is DOWN. Perform a reboot after $running seconds of running" >> $log
        sync
        /sbin/ifdown 'wlan0'
        sleep 5
        /sbin/ifup --force 'wlan0'
#	counter=$(cat ${tmpfile})
        /sbin/reboot
    fi
#else
#    echo "$date Network is up and running for $running seconds" >> $log
fi
