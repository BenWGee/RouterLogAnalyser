#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 13:32:59 2023

@author: bengee
"""

import re
import csv

#==============================================================================
def checkForNewDevices(newDevices, oldDevices):
    """
    Parameters
    ----------
    newDevices : set
        Data retrieved from most recent log pull.
    oldDevices : set
        Known device list from previous run.

    Returns
    -------
    unknownDevices, set of devices that appear in the new logs, but not in 
    the old devices

    """
    # Unknown devices is the set of all devices kess the set of old devices
    unknownDevices = newDevices - oldDevices
    
    return unknownDevices
#==============================================================================


#==============================================================================
def getDetailsFromLog(log,searchPattern):
    """

    Parameters
    ----------
    log : String
        Network log data
    searchPattern : String
        Regex pattern to match         
        
    Returns
    -------
    wifiDevices, set of MAC addresses of wifi devices
    
    """
    # Use re to find all instances of the given search pattern
    macAddresses = set(re.findall(searchPattern, log))
    
    return macAddresses
#==============================================================================

#==============================================================================
def getMACDetails(addr):
    """
    

    Parameters
    ----------
    addr : String
        MAC address of some device
        
    Returns
    -------
    vendor : String
        The name of the vendor associated with some MAC address.
        Otherwise "Unknown Vendor" is returned. This is not a problem. 
        Some devices are not listed in the file for one reaosn or another. 

    """
    
    # Assume vendor is unknown
    vendor = "Unknown Vendor"
    # Open a flat file of MAC address prefixes, prefixes are static per company
    # Can download file here: https://maclookup.app/search/result?mac=D2:9F:83:97:F6:41
    with open('mac-vendors-export.csv', 'rt') as f:
         reader = csv.reader(f, delimiter=',')
         for row in reader:
             # Prefixes are not a fixed length
             # Make prefix by getting substring of the full address
             prefix = addr[0:len(row[0])]
             # Check f the item in the current row, column 0 matches the prefix
              if row[0] == prefix:
                  # If a match is found vendor info is in column 1
                  vendor = row[1]
                  
    return vendor
#==============================================================================

# Target log file
fileName = "logFile"
#regex pattern to extract MAC Addresses
searchPattern = "(?<=<).{17}(?=>)"

# Open the log file
with open(fileName, 'r') as file:
    logs = file.read().replace('\n', '')

# Call function to return all MAC addresses in logs
macAddr = getDetailsFromLog(logs, searchPattern)

for addr in macAddr:
    print(f"{addr} is associated with: {getMACDetails(addr)}")
    
    
    
