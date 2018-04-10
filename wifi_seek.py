#!/usr/bin/python3

# TODO Ensure getIp() does not return None... or check calls for when it might.

"""/
THIS SCRIPT MUST RUN WITH SUPER USER PERMISSIONS

Derek Snyder
Mon  2 Apr 22:32:31 UTC 2018
"""

import subprocess
import re
import time

# get current WiFi network name
#   iwgetid -r
def currentNetwork():
    return subprocess.check_output(
            'iwgetid -r'.split()
    ).decode('utf-8')

# scan for available WiFi networks
#   sudo iwlist wlan0 scan
def availableNetworks( allowNewlines=False ):
    scanOutput = subprocess.check_output(
            'iwlist wlan0 scan'.split()
    ).decode('utf-8')
    # TODO parse output into list of AP objects
    if not allowNewlines:
        scanOutput = scanOutput.replace('\n', '')

    return scanOutput

# listed in ifconfig wlan0 output
def getIp():
    ifconfigOutput = subprocess.check_output(
            'ifconfig wlan0'.split()
    ).decode('utf-8')
    #print(ifconfigOutput)
    ipRegex = r'inet ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})'
    if re.search(ipRegex, ifconfigOutput):
        return re.search(ipRegex, ifconfigOutput).group(1)
    else:
        return ""


def fastFindNetworks(scanOutput ):
    essid_regex = re.compile(r'ESSID:"([A-Za-z0-9|\-]+)"')
    matches = essid_regex.findall( scanOutput)
    return matches

# TODO refactor return codes
# TODO 

if __name__ == '__main__':
    
    import sys

    if len(sys.argv) == 3:
        _TARGET_ESSID = sys.argv[1]
        _TARGET_PSK = sys.argv[2]
    else:
        print("Usage: wifi_seek.py [access point name] [access point password]")
        quit()

    '''/
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
        print('Already connected to target. IP %s' % getIp() )
        quit(3)

    # pi is not connected to any WiFi networks
    ffn = fastFindNetworks( availableNetworks() )
    for network in ffn:
        print(network)
    #input("what's goin on? ... debugging, that's what.")
    if _TARGET_ESSID not in ffn:
        # target not in range
        print('Target ESSID \'%s\' not in range.' % _TARGET_ESSID )
        quit(1)

    '''/
    Attempt to connect with special network--
        this is done using wpa_passphrase command:
            wpa_passphrase "essid" "psk" >> /etc/wpa_supplicant/wpa_supplicant.conf
            (or)
            wpa_passphrase "essid" "psk" | sudo tee -a /etc/wpa_supplicant.conf > /dev/null
        then reconfigure interface:
            wpa_cli -i wlan0 reconfigure
    '''
    # TODO utilize wifi_reconfig.sh program to handle the reconnecting
    returnVal = subprocess.check_output(
            ('/home/pi/wifi_reconfig.sh %s %s' % (_TARGET_ESSID, _TARGET_PSK)).split()
    ).decode('utf-8')
    print('wifi_reconfig.sh returned %s' % returnVal)

    # check up to 5 times if connection was successful
    connectionSuccess = False
    for retryCounter in range(5):
        time.sleep(5)
        ip = getIp()
        if ip != None and ip != '': # TODO this shouldn't be returning 'None'
            connectionSuccess = True
            break
        else:
            print('%d: IP address not yet acquired. Retrying...' % retryCounter)
            pass

    if connectionSuccess:
        '''
        Code to run once connected goes here
        '''
        print('Connection successful. IP %s' % getIp() )
        pass
    else:
        print('Retry limit reached, no network connection established. Exiting')
        quit(3)

    #print( getIp() )

