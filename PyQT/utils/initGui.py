import os
import sys

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

from utils.mainWindow import Ui_MainWindow
from utils.data import Data
from utils import functions

from ipaddress import ip_address, IPv4Address, IPv6Address
import subprocess


class GUI:
    def __init__(self, path):
        self.closed = False
        self.statusbar_is_hide = True
        self.path = path
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.data = Data('{}/utils/Data.json'.format(path))

    def init_main_window(self):
        # Set icon
        self.set_button_icon(self.ui.apply_button,
                             '{}/icon/apply.png'.format(self.path))
        self.set_button_icon(self.ui.fastest_button,
                             '{}/icon/fastest.png'.format(self.path))
        self.set_button_icon(self.ui.ping_button,
                             '{}/icon/ping.png'.format(self.path))
        self.set_button_icon(self.ui.save_button,
                             '{}/icon/save.ico'.format(self.path))
        self.set_button_icon(self.ui.remove_button,
                             '{}/icon/remove.png'.format(self.path))

        # set icon title
        self.MainWindow.setWindowIcon(QtGui.QIcon(os.path.join(
            sys.path[0], "{}/icon/dns-logo.png".format(self.path))))

        # Load Network list
        for index, network in enumerate(self.data.data['interfaces']):
            self.ui.network_selection.addItem(network['name'])
            self.set_network_icon(self.ui.network_selection,
                                  index,
                                  network['state'])

        self.select_network_combo_box_changed(
            self.data.data['settings']['network'])

        # Load DNS list
        for dns in self.data.data['dns_list']:
            self.ui.dns_selection_combo_box.addItem(dns['name'])
        self.select_dns_combo_box_changed(self.data.data['settings']['dns'])

        # Init statusBar
        self.ui.statusBar = QtWidgets.QStatusBar(self.MainWindow)
        self.ui.statusBar.setObjectName("Statfus bar")
        self.MainWindow.setStatusBar(self.ui.statusBar)
        self.ui.statusBar.hide()
        self.ui.statusBar.setStyleSheet('color: #000; background-color: #fff')

        # Signals
        self.ui.apply_button.clicked.connect(self.apply_dns)
        self.ui.fastest_button.clicked.connect(self.start_fastest_window)
        self.ui.ping_button.clicked.connect(self.calc_current_dns_ping)
        self.ui.ipv4_primary_line_edit.textChanged.connect(
            self.primary_changed)
        self.ui.ipv4_secondary_line_edit.textChanged.connect(
            self.secondary_changed)
        self.ui.dns_selection_combo_box.currentIndexChanged.connect(
            self.select_dns_combo_box_changed)

    def add_item_to_table(self, table, dns):
        row_count = table.rowCount()
        table.setRowCount(row_count + 1)
        table.setItem(row_count, 0, QTableWidgetItem(dns['name']))
        table.setItem(row_count, 1, QTableWidgetItem(dns['primary_ip']))
        table.setItem(row_count, 2, QTableWidgetItem(dns['secondary_ip']))
        table.setItem(row_count, 3, QTableWidgetItem(dns['primary_ping']))
        table.setItem(row_count, 4, QTableWidgetItem(dns['secondary_ping']))
        table.setItem(row_count, 3, QTableWidgetItem(dns['primary_ping']))
        table.setItem(row_count, 4, QTableWidgetItem(dns['secondary_ping']))

    # Set icon for button
    @staticmethod
    def set_button_icon(button, icon_path):
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(icon_path),
                       QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        button.setIcon(icon)

    # Set icon for item
    # @staticmethod
    def set_network_icon(self, network, index_item, state):
        icon = QtGui.QIcon()
        if state == "Connected":
            icon_online_path = '{}/icon/online1.png'.format(self.path)
            icon.addPixmap(QtGui.QPixmap(icon_online_path),
                           QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        else:
            icon_offline_path = '{}/icon/offline1.png'.format(self.path)
            icon.addPixmap(QtGui.QPixmap(icon_offline_path),
                           QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        # network.setPixmap(icon.pixmap(64, 64))
        network.setItemIcon(index_item, icon)
        network.setIconSize(QSize(12, 12))
        network.setStyleSheet("""
            QComboBox {
                padding: 5px 5px 5px 8px;  
            }                    
        """)

    # Statusbar
    def send_status_bar_message(self, text):
        if self.statusbar_is_hide:
            self.statusbar_is_hide = False
            self.ui.statusBar.show()
        self.ui.statusBar.showMessage(text)

    # Apply DNS
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
                self.send_status_bar_message("{} applied successfully".format(
                    self.data.data['dns_list'][self.data.data['settings']['dns']]['name']))

        except subprocess.CalledProcessError as e:
            print(e)
            functions.print_c("can't apply DNS!", functions.Bcolors.FAIL)
        except Exception as e:
            print(e)
            functions.print_c("can't apply DNS!", functions.Bcolors.FAIL)

    def start_fastest_window(self):
        print("start_fastest_window")

    # Show DNS Ping
    def calc_current_dns_ping(self):
        primary_ping = functions.ping(
            server=self.ui.ipv4_primary_line_edit.text())
        secondary_ping = functions.ping(
            server=self.ui.ipv4_secondary_line_edit.text())
        primary_ipv6_ping = functions.ping6(
            server=self.ui.ipv6_primary_line_edit.text())
        secondary_ipv6_ping = functions.ping6(
            server=self.ui.ipv6_secondary_line_edit.text())
        if primary_ping:
            primary_ping = int(float(primary_ping['avg']))
        if primary_ipv6_ping:
            primary_ipv6_ping = int(float(primary_ipv6_ping['avg']))
        else:
            print("Not found")
            # primary_ping = False
            # primary_ipv6_ping = False
        if secondary_ping:
            secondary_ping = int(float(secondary_ping['avg']))
        if secondary_ipv6_ping:
            secondary_ipv6_ping = int(float(secondary_ipv6_ping['avg']))
        else:
            print("Not found")
            # secondary_ping = False
            # secondary_ipv6_ping = False

        self.send_status_bar_message('{} => Primary: {} | Secondary: {} | IPv6 Primary: {} | IPv6 Secondary: {}'.format(
            self.data.data['dns_list'][self.data.data['settings']
                                       ['dns']]['name'],
            primary_ping,
            secondary_ping,
            primary_ipv6_ping,
            secondary_ipv6_ping
        ))

    # Check if ip is valid
    @staticmethod
    def valid_ip_address(ip):
        try:
            if type(ip_address(ip)) is IPv4Address or IPv6Address:
                return True
        except ValueError:
            return False

    # Change DNS
    def primary_changed(self):
        if self.valid_ip_address(self.ui.ipv4_primary_line_edit.text()):
            self.ui.ipv4_primary_line_edit.setStyleSheet('color: #009933')
            self.ui.ipv6_primary_line_edit.setStyleSheet('color: #009933')
        else:
            self.ui.ipv4_primary_line_edit.setStyleSheet('color: #e60000')

    def secondary_changed(self):
        if self.valid_ip_address(self.ui.ipv4_secondary_line_edit.text()):
            self.ui.ipv4_secondary_line_edit.setStyleSheet('color: #009933')
            self.ui.ipv6_secondary_line_edit.setStyleSheet('color: #009933')
        else:
            self.ui.ipv4_secondary_line_edit.setStyleSheet('color: #e60000')

    # Network list
    def select_network_combo_box(self, index):
        if index == 1:
            self.ui.network_selection.setDisabled(False)
            self.ui.network_selection.setCurrentIndex(index)
        else:
            self.ui.network_selection.setDisabled(False)

    def select_network_combo_box_changed(self, index):
        self.select_network_combo_box(index)
        self.data.data['settings']['dns'] = index
        self.data.save_changes()

    # DNS list
    def select_dns_combo_box(self, index):
        if index == 1:
            self.ui.remove_button.setDisabled(True)
            self.ui.ipv4_primary_line_edit.setDisabled(False)
            self.ui.ipv4_secondary_line_edit.setDisabled(False)
            self.ui.ipv6_primary_line_edit.setDisabled(False)
            self.ui.ipv6_secondary_line_edit.setDisabled(False)
            self.ui.name_line_edit.setDisabled(False)
            self.ui.dns_selection_combo_box.setCurrentIndex(index)
        elif index == 0:
            self.ui.ipv4_primary_line_edit.setDisabled(True)
            self.ui.ipv4_secondary_line_edit.setDisabled(True)
            self.ui.ipv6_primary_line_edit.setDisabled(True)
            self.ui.ipv6_secondary_line_edit.setDisabled(True)
            self.ui.name_line_edit.setDisabled(True)
            self.ui.remove_button.setDisabled(True)
            self.ui.dns_selection_combo_box.setCurrentIndex(index)
        else:
            self.ui.ipv4_primary_line_edit.setDisabled(False)
            self.ui.ipv4_secondary_line_edit.setDisabled(False)
            self.ui.ipv6_primary_line_edit.setDisabled(False)
            self.ui.ipv6_secondary_line_edit.setDisabled(False)
            self.ui.name_line_edit.setDisabled(False)
            self.ui.remove_button.setDisabled(False)
            self.ui.dns_selection_combo_box.setCurrentIndex(index)

    def select_dns_combo_box_changed(self, index):
        self.select_dns_combo_box(index)
        self.ui.name_line_edit.setText(
            self.data.data['dns_list'][index]['name'])
        self.ui.ipv4_primary_line_edit.setText(
            self.data.data['dns_list'][index]['primary'])
        self.ui.ipv4_secondary_line_edit.setText(
            self.data.data['dns_list'][index]['secondary'])
        self.ui.ipv6_primary_line_edit.setText(
            self.data.data['dns_list'][index]['primary_ipv6'])
        self.ui.ipv6_secondary_line_edit.setText(
            self.data.data['dns_list'][index]['secondary_ipv6']
        )
        self.data.data['settings']['dns'] = index
        self.data.save_changes()

    # End Program
    def end_program(self):
        self.closed = True

    # Start Program
    def start(self):
        self.init_main_window()
        self.MainWindow.show()
        self.app.aboutToQuit.connect(self.end_program)
        sys.exit(self.app.exec())
