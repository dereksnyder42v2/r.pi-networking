#!/usr/bin/python3

"""
THIS SCRIPT MUST RUN WITH SUPER USER PERMISSIONS

Derek Snyder
Mon  2 Apr 22:32:31 UTC 2018
"""

import subprocess
import re
import time
import codecs

# get current WiFi network name
#   iwgetid -r
def currentNetwork():
    run_instance = subprocess.run( 
            "iwgetid -r".split(),
            stdout=subprocess.PIPE
        )
    # .run() returns a subprocess.CompletedProcess instance
    #       .returncode (usually 0 if successful)
    #       .stdout     (output of process)
    #       .stderr     (error output)
    current_network_output = codecs.decode(run_instance.stdout, 'utf-8').replace('\n', '')

    return current_network_output

# scan for available WiFi networks
#   sudo iwlist wlan0 scan
def available_networks( allow_newlines=False ):
    run_instance = subprocess.run(
            "iwlist wlan0 scan".split(),
            stdout=subprocess.PIPE
    ) 
    scan_output = codecs.decode(run_instance.stdout, "utf-8")
    if not allow_newlines:
        scan_output = scan_output.replace("\n", "")
    
    return scan_output

# listed in ifconfig wlan0 output
def getIp():
    run_inst = subprocess.run(
            "ifconfig wlan0".split(),
            stdout=subprocess.PIPE
    )
    ifconfigOutput = codecs.decode(run_inst.stdout, "utf-8")
    ipRegex = r"inet ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})"
    if re.search(ipRegex, ifconfigOutput):
        return re.search(ipRegex, ifconfigOutput).group(1)
    else:
        return ""


def list_networks(scanOutput ):
    print("Warning: only ESSIDs containing characters A-Z, a-z, 0-9, hyphen (-), and period (.) are allowed!")
    essid_regex = re.compile(r"ESSID:\"([A-Za-z0-9|\-|\.]+)\"")
    matches = essid_regex.findall( scanOutput)
    
	return matches


if __name__ == '__main__':
    
    import sys
    import os    

    # check if user is root. Program won't work without
    if os.geteuid() != 0:
        print("Current user is not root; unable to do anything useful. Exiting")
        quit()

    # check proper script usage
    if len(sys.argv) == 3:
        _TARGET_ESSID = sys.argv[1]
        _TARGET_PSK = sys.argv[2]
    else:
        print("Usage: wifi_seek.py [access point name] [access point password]")
        quit()
    
    # TODO refactor return codes
    '''
    program control flow

    1. check if Pi is currently connected to any network
        - if connection already present, halt
        - else go to step 2
    2. scan all networks in range
        - if our special network is not present, halt
        - else go to step 3
    3. attempt connection with special network
    4. wait some time for handshake
    5. check if Pi has acquired IP address
        - if no IP yet: decrement retryCounter, go back to 4
        - if IP is present: finished
        - if no IP and retryCounter is 0, halt

    program return codes

    0: pi is
    1: pi isn't connected, target network not in range
    2: target network found; connection attempted, but failed
    3: pi is already connected
    '''

    if currentNetwork() == _TARGET_ESSID:
        # pi is already connected. nothing to do here
        print("Already connected to target. IP address = %s" % (getIp()) )
        quit(3)

    # pi is not connected to any WiFi networks
    networks = list_networks( available_networks() )
    for network in networks:
        print(network) 
    if _TARGET_ESSID not in networks:
        # target not in range
        print("Target ESSID '%s' not in range." % (_TARGET_ESSID) )
        quit(1)

    '''
    Attempt to connect with special network--
        this is done using wpa_passphrase command:
            wpa_passphrase "essid" "psk" >> /etc/wpa_supplicant/wpa_supplicant.conf
            (or)
            wpa_passphrase "essid" "psk" | sudo tee -a /etc/wpa_supplicant.conf > /dev/null
        then reconfigure interface:
            wpa_cli -i wlan0 reconfigure
    ''' 

    returnVal = codecs.decode(
            subprocess.run(
                ("%s/wifi_reconfig.sh %s %s" % (os.getcwd(), _TARGET_ESSID, _TARGET_PSK)).split(),
                stdout=subprocess.PIPE).stdout,
            'utf-8'
    )
    
    print("wifi_reconfig.sh returned %s" % returnVal)

    # check up to 5 times if connection was successful
    connectionSuccess = False
    for retryCounter in range(5):
        time.sleep(5)
        ip = getIp()
        if ip != None and ip != '': # TODO this shouldn't be returning 'None'
            connectionSuccess = True
            break
        else:
            print("%d: IP address not yet acquired. Retrying..." % retryCounter)
            pass

    if connectionSuccess:
        '''
        !!! Code to run once connected goes here !!!
        '''
        print("Connection successful. IP %s" % getIp() )
        pass
    else:
        print("Retry limit reached, no network connection established. Exiting")
        quit(3)

