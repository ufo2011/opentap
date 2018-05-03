#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Authors: Christian Macias and Michael P. McGarry

Description: Python script that auto-generates the opentap.conf by interviewing the installer

"""
from subprocess import check_output as chkout
import os

print("\nCreating the opentap.conf file to configure the behavior of OpenTap.\n")
print("We will solicit input from you to complete this process.\n")

art = """
######  #####  ###### ##    #      #######     #      ##### 
#    #  #   #  ##     # #   #         #       # #     #   # 
#    #  #####  #####  #  #  #         #      #   #    ##### 
#    #  ##     ##     #   # #         #     #######   ##    
######  ##     ###### #    ##         #    #       #  ##    

#############################################################
"""

information = """
## All Configurable options are available in this file
"""

#create the conf file
try:
    f = open("etc/opentap/opentap.conf", "w+")
    
except:
    print("Unable to open opentap.conf")
    exit(1)

#Write heading information
f.write(art)
f.write(information)

#Parameter: retention period
retentionComment = """
# Data retention period - Number of minutes to retain collected data
#
"""
retentionPeriod = raw_input("Enter desired data retention period (in minutes): ")
retentionParameter = "retention: " + str(retentionPeriod)
f.write(retentionComment)
f.write(retentionParameter)

#Parameter: Web address
webaddrComment = """
# IP address to for the webserver to run on.
# For example: 127.0.0.1:80 
"""
webAddr = raw_input("Enter the address for OpenTap's web interface as IPaddr:portnum (e.g., 127.0.0.1:80): ")
webaddrParameter = "websrv-addr: " + webAddr
f.write("\n")
f.write(webaddrComment)
f.write(webaddrParameter)
f.write("\n")


# default network observation point will be the first one be returned by ifconfig, can be changed by the user later
listenComment = """
# Default network observation point (used if one is not specified in /capture invocation) 
"""
observationPtParameter = "default-network-observationpt: "
interfaces           = chkout(["/sbin/ifconfig"])
interfaces           = interfaces.decode("UTF-8")
interfaces           = interfaces.split("\n\n")
defaultInterface     = interfaces[0].split("\n")
defaultInterfaceName = (defaultInterface[0].split())[0]
defaultInterfaceName = defaultInterfaceName.replace(":", "") #Remove colon. Important with centos

f.write("\n")
f.write(listenComment)
f.write(observationPtParameter + defaultInterfaceName)

#Interface alias
aliasComment = """

# Aliases for network interfaces (used in the observationPt parameter to /capture invocation)
"""
f.write(aliasComment)
if(len(interfaces) == 1):
    #There is no interfaces....
    f.write("""#No interfaces detected during installation.""" + "\n")
    f.write("""#alias: eth0 mirror\n""" + "\n")
    f.write("""#alias: eth1 webapp""" + "\n")
else:
    print("\n" + "Enter aliases for detected network interfaces:" + "\n")
    for iface in interfaces:

        try:
            interfaceDetails     = iface.split("\n")
            interfaceName = (interfaceDetails[0].split())[0]
            interfaceName = interfaceName.replace(":", "")
            os.mkdir("/opt/opentap/log/" + interfaceName)
        except OSError:
            if(not os.path.isdir("/opt/opentap/log/" + interfaceName)):
                print("OSError: Unable to create directory \"/opt/opentap/log/" + interfaceName + "\"")
        except:
            #Probably some indexing error.
            continue
        
        if(interfaceName == "lo"):
            pass
        else:
            newAlias = raw_input(interfaceName + " alias" + ": ")
            f.write("alias: " + interfaceName + " " + newAlias + "\n")
    f.write("\n")

f.close()
