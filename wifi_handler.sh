#!/bin/bash

# remember! wifi_seek.py return codes are...
#    0: pi is already connected, or connection attempt successful
#    1: pi isn't connected, target network not in range
#    2: target network found; connection attempted, but failed
#    3: [not used]
#    4: incorrect usage (bad cmd args or uid not sudo)

direc='/home/pi/r.pi-networking'
targetEssid='Blackpearl'
targetPsk='Chungus12'

logfile='/var/log/r.pi-networking/log.txt'
date >> $logfile

cd $direc
if [ $UID -ne 0 ]; then
	echo 'Not root' >> $logfile
	exit
fi

$direc/wifi_seek.py $targetEssid $targetPsk 2>&1 >> $logfile



