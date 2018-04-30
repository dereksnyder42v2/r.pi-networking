#!/bin/bash

# Run this script once to configure the environment for the wifi seeking program

printf 'Author: Derek Snyder (dereksnyder42@gmail.com)\n'

if [ $UID -ne 0 ]; then
	echo 'Must be root. Doing nothing and exiting'
	exit 1
fi

printf '\nChecking dependencies (python3 installation at /usr/bin/python3)...\n'
if [ ! -f '/usr/bin/python3' ]; then
	echo 'No python3 installation found at /usr/bin/python3. Consider making a link, or edit the the shebangs at top of each Python script.'
	exit 1
fi

printf '\nChecking for log file at /var/log/r.pi-networking/log.txt...\n'
if [ ! -f '/var/log/r.pi-networking/log.txt' ]; then
	echo 'Log file not found. Making log at /var/log/r.pi-networking'
	mkdir -p "/var/log/r.pi-networking"
	touch /var/log/r.pi-networking/log.txt
fi

# TODO make install script for init.d process


printf "\nChecking that wifi_handler.sh has proper path...\n"
sed -i "/^direc.*/c direc='${PWD}'" wifi_handler.sh


