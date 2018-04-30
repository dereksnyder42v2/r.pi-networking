# r.pi-networking
(Generally, I think all of the programs here need super used permissions, simply because accessing the init system and network interface are privileged operations.)

This is a project to reliably and controllably connect to a designated WiFi network when the host system (a Raspberry Pi) may be traveling in and out of range of the desired network.
It is intended to be run as a persistent 'init' process, checking network settings and searching for the target WiFi network every 10 minutes. Future versions of Debian may further change the 'init' structure, favoring the SystemD model--a SystemD service file could be made instead as need or preference arise. 
Most operation is handled in the 'wifi_handler.sh' shell script--namely, network checking intervals (10 minutes by default), calling of the 'wifi_seek.py' script, and logging behavior.

Run the 'config.sh' file once; this creates the log file, configures the init process, etc. 
Change the targetEssid and targetPsk values in 'wifi_handler.sh' to whatever network you wish to search for & connect to. If a strong network connection is present but the scans aren't picking it up, you might check the regular expression in 'wifi_seek.py' 
Change the 'sleep 10m' command in 'wifi_handler.sh' to whatever time interval you wish to check network configuration at.

File descriptions:
- 'r.pi-networking_init' 
this is the init script, which runs persistently in the background. It should be copied into the /etc/init.d/ directory (on Debian), but 'config.sh' does that for you.
- 'wifi_seek.py' 
this file checks networks in range, attempts to connect (by calling 'wifi_reconfig.sh') if the target network is detected, and returns a status  code indicating to the caller what exactly happened (0 is success).
- 'wifi_reconfig.sh' 
this file writes a new wpa_supplicant.conf, then brings down & brings up the wlan0 networking interface on the system. It is called by 'wifi_seek.py'. My $0.02, don't even try to make this work for a different interface/ USB-WiFi adapter/ etc. 
- 'wifi_handler.sh' 
this is the script which is executed by init process, and is probably the only thing you want to modify for normal use (: It is responsbible for calling 'wifi_seek.py' and logging return codes with timestamps (may be useful for debugging).
- 'stream_video.py' 
oddball program I threw in, as an example for what you might want to do once network is established. It runs a server, streaming Raspberry Pi camera footage viewable in a web browser of a local PC.   
- 'tests.py' 
this program gives examples of the types of output 'wifi_seek.py' functions may return, such as networks in range, current IP address and WiFi network name, etc.

