#!/usr/bin/env python3

#--------------------------------------------------------------------------------
# This script will interrogate the RIPEStat API for BGP looking glass information
#--------------------------------------------------------------------------------

import requests
import json
import re

#-------------------------------------------
# Ask user to enter a BGP AS Number to query
#-------------------------------------------

def user_input():
    as_number = input('Enter a BGP AS number: ')
    global as_int
    try:
        as_int=int(as_number)
    except ValueError:
        print('Please enter a number')

#-------------------------------------------------
# Validate that user entered a valid BGP AS Number
#-------------------------------------------------

def user_input_validation(as_int):

    #Data validation
    if (as_int >=1 and as_int <= 64511):
        print('This is a BGP 2-byte public AS number')
    elif (as_int >=64512 and as_int <=65535):
        print('This is a BGP 2-byte private AS number')
    elif (as_int >= 65536 and as_int <=4294967296):
        print('This is a BGP 4-byte AS number')
    else:
        print('''
          Please enter a valid AS number
          Acceptable Public AS numbers are as follows:
          2 Byte AS Number range: 1 - 64511
          4 bytes AS Number range: 65536-4294967296
          ''')
        user_input()

#-----------------------------------------
# Get prefix information from RIPEStat API
#-----------------------------------------

def get_prefixes(as_int):

    response = requests.get("https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS%s" % as_int)
    data = json.loads(response.text)
    for entry in data['data']['prefixes']:
        if re.search(':', entry["prefix"]):
            print('IPv6 Prefix: %s' % entry["prefix"])
        else:
            print('IPv4 Prefix: %s' % entry["prefix"])

#-----------------------------------------
# Main
#-----------------------------------------

print('''
--------------------------------------------------------------------------------------------
This script will discover all prefixes currently being announced by a BGP Autonomous System
--------------------------------------------------------------------------------------------
''')
user_input()
user_input_validation(as_int)
print('''
--------------------------------------------------------------------------------
The following prefixes are currently being announced by BGP AS %s
--------------------------------------------------------------------------------
''' % as_int)
get_prefixes(as_int)
