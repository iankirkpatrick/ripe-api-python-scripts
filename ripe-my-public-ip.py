#!/usr/bin/env python3

#--------------------------------------------------------------------------------
# This script will interrogate the RIPEStat API for your public IP information
#--------------------------------------------------------------------------------

import requests
import json
import re

#-------------------------------------------------------------------------------
# Query RIPE for Public IP
#-------------------------------------------------------------------------------
query = requests.get("https://stat.ripe.net/data/whats-my-ip/data.json")
data = json.loads(query.text)

#-------------------------------------------------------------------------------
# Display banner
#-------------------------------------------------------------------------------
print('''
--------------------------------------------------------------------------------------------
Querying RIPE Servers for your public IP address
--------------------------------------------------------------------------------------------''')

#-------------------------------------------------------------------------------
# Query RIPE API to find out which AS originated the IP address
#-------------------------------------------------------------------------------

ipinfo = requests.get("https://stat.ripe.net/data/network-info/data.json?resource=%s" % data['data']['ip'])
ipinfo_data = json.loads(ipinfo.text)
as_number = ipinfo_data['data']['asns']
as_text = ''.join(as_number)

#-------------------------------------------------------------------------------
# Query RIPE API for background information on AS
#-------------------------------------------------------------------------------

asinfo = requests.get("https://stat.ripe.net/data/as-overview/data.json?resource=AS%s" % as_text)
asinfo_data = json.loads(asinfo.text)

#-------------------------------------------------------------------------------
# Display the result
#-------------------------------------------------------------------------------

print('''
Your public IP address is %s
Which is part of the address block %s advertised by BGP AS %s
Which is registered to %s
--------------------------------------------------------------------------------------------
''' % (data['data']['ip'],ipinfo_data['data']['prefix'],as_text,asinfo_data['data']['holder']))
