from utils.data import Data
import subprocess
import json
from utils import functions

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import *


class Haha:
    def __init__(self, path):
        self.data = Data('{}/utils/Data.json'.format(path))

    def apply_dns(self):
        try:
            settins_dns = self.data.data['settings']['dns']
            interface_name = self.data.data['interfaces'][self.data.data['settings']
                                                          ['network']]['name']
            # Set DHCP DNS
            if settins_dns == 0:
                subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'dns',
                               interface_name, 'dhcp'], check=True)

                subprocess.run(['netsh', 'interface', 'ipv6', 'set', 'dns',
                                interface_name, 'dhcp'], check=True)
            else:
                primary = self.data.data['dns_list'][self.data.data['settings']
                                                     ['dns']]['primary']
                secondary = self.data.data['dns_list'][self.data.data['settings']
                                                       ['dns']]['secondary']
                primary_ipv6 = self.data.data['dns_list'][self.data.data['settings']
                                                          ['dns']]['primary_ipv6']
                secondary_ipv6 = self.data.data['dns_list'][self.data.data['settings']
                                                            ['dns']]['secondary_ipv6']
                # Set Primary DNS
                if primary:
                    subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'dns',
                                    interface_name, 'static', primary], check=True, shell=True)
                    subprocess.run(['netsh', 'interface', 'ipv6', 'set', 'dns',
                                    interface_name, 'static', primary_ipv6], check=True, shell=True)

                # Set Secondary DNS
                if secondary:
                    subprocess.run(['netsh', 'interface', 'ipv4', 'add', 'dns',
                                    interface_name, secondary, 'index=2'], check=True, shell=True)
                    subprocess.run(['netsh', 'interface', 'ipv6', 'add', 'dns',
                                    interface_name, secondary_ipv6, 'index=2'], check=True, shell=True)

        except subprocess.CalledProcessError as e:
            print(e)
            functions.print_c("can't apply DNS!", functions.Bcolors.FAIL)
        except Exception as e:
            print(e)
            functions.print_c("can't apply DNS!", functions.Bcolors.FAIL)
