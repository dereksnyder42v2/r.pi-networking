#!/bin/bash

# THIS SCRIPT REQUIRES SU PERMISSIONS TO RUN
# params:
#	- $1	ESSID
#	- $2 	PSK

ESSID=$1
PSK=$2

cat <<EOF > /etc/wpa_supplicant/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

EOF

wpa_passphrase "$ESSID" "$PSK" >> /etc/wpa_supplicant/wpa_supplicant.conf

wpa_cli -i wlan0 reconfigure

exit 0
