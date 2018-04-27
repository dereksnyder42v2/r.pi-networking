#!/bin/bash

# Run this script once to configure the environment for the wifi seeking program

printf 'Author: Derek Snyder (dereksnyder42@gmail.com)\n'

if [ $UID -ne 0 ]; then
	echo 'Must be root. Doing nothing and exiting'
	exit 1
fi

printf '\nChecking dependencies (python3 installation at /usr/bin/python3)...\n'
if [ ! -f '/usr/bin/python3' ]; then
	echo 'No python3 installation found at /usr/bin/python3. Consider making a link, or fork this repository and change the shebang at top of scripts.'
	exit 1
fi

printf '\nChecking for log directory at /var/log/r.pi-networking...\n'
if [ ! -d '/var/log/r.pi-networking' ]; then
	echo 'Log dir not found. Making log directory at /var/log/r.pi-networking'
	mkdir -p "/var/log/r.pi-networking"
fi

crontab_cmd="*/10 * * * * $PWD/wifi_handler.sh"
printf "\nChecking for cron job ($crontab_cmd) in super user crontab...\n"
crontab -l | grep "wifi_handler.sh"
if [ $? -ne 0 ]; then
	echo 'Adding new cron job.'
	crontab -l > mycron
	echo "$crontab_cmd" >> mycron
	crontab mycron
	rm mycron
fi

printf "\nChecking that wifi_handler.sh has proper path...\n"
sed -i "/\$direc.*/c direc='${PWD}'" wifi_handler.sh
