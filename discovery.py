
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
dev = sys.argv[2]

os.system('mkdir Reports')
report_folder = 'Reports'
class Discover():

    def __init__(self):
        with open('mapping.yaml') as f:
              o = yaml.safe_load(f)
        self.testbed = load('inventory.yaml')
        self.site = site
        self.hostname = dev
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
        with open("testmap.yaml") as file:
            o = yaml.load(file, Loader=yaml.FullLoader)
            devices = o['sites'][site]['devices']
        for devices, key in devices.items():
            a=key['ip_pools']
            voicevlan=a[0]['voicevlan']
            voiceippool=a[0]['voiceippool']
            input=1
            datavlan=a[1]['vlan2']
            datapool=a[1]['ippool2']
            # vlanid3=a[2]['vlan3']
            # poolname3=a[2]['ippool3']

        with open(report_folder+'/'+date_time_now+self.site+'_input.csv', 'w') as f:
            print('writing data from outputs into input.csv')
            fieldnames = 'Input','hostName','interfaceName','dataIpAddress','voiceIpAddress','authenticate','interfaceDescription','sgt','siteNameHierarchy','deviceManagementIpAddress'
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for key, value in self.report['interfaces'].items():
                interface = key
                description = value['interfaceDescription']
                vlan = value['vlan']
                if str(voicevlan) == str(vlan):
                    print('made it here! - VOICE VLAN')
                    writetocsv = { 'Input': input,
                    'interfaceName': interface,
                    'interfaceDescription': description,
                    'voiceIpAddress': voiceippool,
                    'authenticate': 'Closed Authentication',
                    'hostName': dev,
                    }
                    input = input + 1
                    writer.writerow(writetocsv)
                    
                elif str(datavlan) == str(vlan):
                    interface = key
                    description = value['interfaceDescription']
                    vlan = value['vlan']
                    writetocsv = {'interfaceName': interface,
                    'interfaceDescription': description,
                    'dataIpAddress': datapool,
                    'authenticate': 'Closed Authentication',
                    'hostName': dev,
                    }
                    writer.writerow(writetocsv)

                # elif str(vlanid3) == str(vlan):
                #     interface = key
                #     description = value['interfaceDescription']
                #     vlan = value['vlan']
                #     writetocsv = {'interfaceName': interface,
                #     'interfaceDescription': description,
                #     'dataIpAddress': poolname3,
                #     'authenticate': 'Closed Authentication',
                #     'hostName': dev,
                #     }
                #     writer.writerow(writetocsv)
                else:
                    interface = key
                    description = value['interfaceDescription']
                    vlan = value['vlan']
                    writetocsv = {'interfaceName': interface,
                    'interfaceDescription': description,
                    'dataIpAddress': vlan,
                    'authenticate': 'Closed Authentication',
                    'hostName': dev,
                    }
                    writer.writerow(writetocsv)

    # def edit_indexes(self):
    #     #INSERT LOGIC HERE TO ADD Index values to the Input Column, 
    #     #starting at 1 and running until the end of the dynamic range



if __name__ == '__main__':
    discover = Discover()
    discover.generate_spreadsheet()
#    discover.edit_indexes()