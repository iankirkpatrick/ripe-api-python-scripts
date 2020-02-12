#!/usr/bin/env python3

#---------------------------------------------------------------------------------------
# This script will interrogate the RIPEStat API for information about a given IP address
#---------------------------------------------------------------------------------------

import requests
import json
import re

#-------------------------------------------
# Ask user to enter a public IP address
#-------------------------------------------

def user_input():
    global ip_address
    ip_address = input('Enter the IP address to query: ')

#-------------------------------------------------------------------------------
# Query RIPE API to find out which AS originated the IP address
#-------------------------------------------------------------------------------

def query_ripe(ip_address):
    ipinfo = requests.get("https://stat.ripe.net/data/network-info/data.json?resource=%s" % ip_address)
    ipinfo_data = json.loads(ipinfo.text)
    if (ipinfo_data['data']['asns'] == []):
        as_text = 'None'
        asinfo_result = 'No AS information found'
    else:
        as_number = ipinfo_data['data']['asns']
        as_text = ''.join(as_number)

#-------------------------------------------------------------------------------
# Query RIPE API for background information on AS
#-------------------------------------------------------------------------------

        asinfo = requests.get("https://stat.ripe.net/data/as-overview/data.json?resource=AS%s" % as_text)
        asinfo_data = json.loads(asinfo.text)
        asinfo_result = asinfo_data['data']['holder']

#-------------------------------------------------------------------------------
# Query RIPE API for reverse DNS lookup on IP
#-------------------------------------------------------------------------------

    rev_dns = requests.get("https://stat.ripe.net/data/reverse-dns-ip/data.json?resource=%s" % ip_address)
    rev_dns_data = json.loads(rev_dns.text)
    rev_dns_result = rev_dns_data['data']['result']

    # Deal with empty list which cannot be converted to string using join

    if (rev_dns_result == None):
        rev_dns_record = 'No reverse record found'
    else:
        rev_dns_record = ''.join(rev_dns_result)

#-------------------------------------------------------------------------------
# Query RIPE API for Geolocation data on IP
#-------------------------------------------------------------------------------

    geoloc = requests.get("https://stat.ripe.net/data/geoloc/data.json?resource=%s" % ip_address)
    geoloc_data = json.loads(geoloc.text)
    location = geoloc_data['data']['located_resources']
    location_data = dict(location[0])
    locations=location_data['locations']
    country_data=locations[0]
    country=country_data['country']
#-------------------------------------------------------------------------------
# Display the results
#-------------------------------------------------------------------------------

    print('''
Results for IP address: %s
CIDR address block: %s
Announced by BGP AS: %s
Registration information: %s
Reverse DNS Lookup: %s
Geolocation country: %s''' % (ip_address,ipinfo_data['data']['prefix'],as_text,asinfo_result,rev_dns_record,country))

    print('''
--------------------------------------------------------------------------------------------
    ''')

#-------------------------------------------------------------------------------
# Main function
#-------------------------------------------------------------------------------

print('''
--------------------------------------------------------------------------------------------
This script will gather background information on an IP address using the RIPEStat API
''')
user_input()
query_ripe(ip_address)
