
#!/usr/bin/env python
__version__ = "0.2"
__author__ = "Daniel Brooker"
__author_email__ = "dabrooke@cisco.com"
__copyright__ = "Copyright (c) 2023 Cisco Systems. All rights reserved."
__license__ = "MIT"


import sys

from genie.conf.base import Device
import pprint
from pyats.topology.loader import load

import csv
import yaml
import pprint
import os
from datetime import datetime

date_time_now =  datetime.now().strftime("%d_%m_:%M")

site = sys.argv[1]

os.system('mkdir Reports')
report_folder = 'Reports'
class Discover():

    def __init__(self):
        with open('mapping.yaml') as f:
              o = yaml.safe_load(f)
        self.testbed = load('inventory.yaml')
        self.site = site
        self.hostname = o['sites'][site]['devices']['hostname']
        device = self.testbed.devices[self.hostname]
        device.connect(init_exec_commands=[], init_config_commands=[])
        self.intdesc = device.parse('show interfaces description')
        self.intstatus = device.parse('show interfaces status')
        self.merge = {}
        
        for interface, values in self.intdesc['interfaces'].items():
            self.merge[interface] = {'description': values['description']}
            if interface in self.intstatus['interfaces']:
                self.merge[interface]['vlan'] = self.intstatus['interfaces'][interface]['vlan']
        
        self.mergedwithkey = {'interfaces': self.merge}


        self.parsed_dict = {}
        for key, value in self.mergedwithkey['interfaces'].items():
            if not key.startswith('Vlan'):
                if 'vlan' not in value:
                    value['vlan'] = ''
                self.parsed_dict[key] = {
                    'interfaceDescription': value['description'],
                    'vlan': value['vlan'],
                }
            self.report = {'interfaces': self.parsed_dict}

    def generate_spreadsheet(self):
        with open(report_folder+'/'+date_time_now+self.site+'_input.csv', 'w') as f:
            print('writing data from outputs into input.csv')
            fieldnames = 'interfaceName','interfaceDescription','dataIpAddressPoolName'
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for key, value in self.report['interfaces'].items():
                interface = key
                description = value['interfaceDescription']
                vlan = value['vlan']
                writetocsv = {'interfaceName': interface,
                'interfaceDescription': description,
                'dataIpAddressPoolName': vlan,
                }
                writer.writerow(writetocsv)

            

if __name__ == '__main__':
    discover = Discover()
    discover.generate_spreadsheet()
