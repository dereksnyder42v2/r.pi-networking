#!/bin/bash

# remember! wifi_seek.py return codes are...
#    0: pi is already connected, or connection attempt successful
#    1: pi isn't connected, target network not in range
#    2: target network found; connection attempted, but failed
#    3: [not used]
#    4: incorrect usage (bad cmd args or uid not sudo)

# $direc should be set by config ... wouldn't hurt to double check ;)
direc='/home/pi/r.pi-networking'
logfile='/var/log/r.pi-networking/log.txt'

cd $direc
if [ $UID -ne 0 ]; then
	echo 'Not root.' >> $logfile
fi

