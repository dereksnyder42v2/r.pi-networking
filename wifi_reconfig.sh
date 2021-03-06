#!/bin/bash

# THIS SCRIPT REQUIRES SU PERMISSIONS TO RUN
# params:
#	- $1	ESSID
#	- $2 	PSK

# check if user is root; quit if not root script would not work!
if [ $UID -ne 0 ]; then
	echo 'User is not root--can`t do anything. Exiting'
	exit 1
elif [ $# -ne 2 ]; then
	echo 'Usage: wifi_reconfig.sh [ESSID] [PSK]. Exiting'
	exit 1
fi

cat <<EOF > /etc/wpa_supplicant/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

EOF

ESSID=$1
PSK=$2
wpa_passphrase "$ESSID" "$PSK" >> /etc/wpa_supplicant/wpa_supplicant.conf

wpa_cli -i wlan0 reconfigure

exit 0
