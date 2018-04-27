#!/usr/bin/python3

import wifi_seek

if __name__ == '__main__':
    import os
    if os.geteuid() != 0:
        print("Not root. Program is useless. Exiting")
        quit()
    
    #test currentNetwork()
    print("Testing currentNetwork()")
    result = wifi_seek.currentNetwork()
    print("\toutput: %s\n\ttype of currentNetwork() output: %s" % (result, type(result)) )

    #test available_networks()
    '''
    print("Testing available_network()")   
    result = wifi_seek.available_networks()
    print("\tresult was", result)
    '''

    #test getIp()
    print("Testing getIp()")   
    result = wifi_seek.getIp()
    print("\toutput: %s\n\ttype of output: %s" % (result, type(result)))

    #test list_networks()
    print("Testing list_networks()")
    result = wifi_seek.list_networks( wifi_seek.available_networks())
    print("\toutput: %s" % (result))

