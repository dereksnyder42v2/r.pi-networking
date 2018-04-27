#!/bin/bash

# remember! wifi_seek.py return codes are...
#    0: pi is already connected, or connection attempt successful
#    1: pi isn't connected, target network not in range
#    2: target network found; connection attempted, but failed
#    3: [not used]
#    4: incorrect usage (bad cmd args or uid not sudo)

direc='/home/pi/r.pi-networking'

cd $direc
