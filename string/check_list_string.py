import os
import sys

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon

from utils.main import Ui_MainWindow

from ipaddress import ip_address, IPv4Address, IPv6Address
import subprocess


class GUI:
    def __init__(self, path):
        self.path = path
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

    def init_main_window(self):
        self.ui.pushButton.clicked.connect(self.get_code)

    def read_file_to_list(self, file_path):
        # Tạo danh sách rỗng để lưu trữ các dòng từ tệp tin
        lines = []
        # Mở tệp tin với chế độ đọc (read mode)
        with open(file_path, 'r', encoding='utf-8') as file:
            # Đọc từng dòng trong tệp tin và thêm vào danh sách
            for line in file:
                # Loại bỏ ký tự xuống dòng (\n) ở cuối mỗi dòng
                lines.append(line.strip())

        return lines

    def check_list(self, file_path, code_input):
        list_code = self.read_file_to_list(file_path)
        for code in list_code:
            if code_input == code:
                return "Có"
        return "Không"

    def change_value_label(self, text):
        self.ui.label.setText(text)

    def get_code(self):
        file_path = "e:\Project\Python\string\list.txt"
        code = self.ui.code_input.text().strip()
        varrient = self.check_list(file_path, code)
        self.change_value_label(varrient)

    def open(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(r'C:/images')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("Images (*.png *.jpg)")
        dialog.setViewMode(QFileDialog.ViewMode.List)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            if filenames:
                print(filenames)
        

    def end_program(self):
        self.closed = True

    def start(self):
        self.init_main_window()
        self.MainWindow.show()
        self.app.aboutToQuit.connect(self.end_program)
        sys.exit(self.app.exec())


if __name__ == "__main__":
    cur_path = sys.path[0]
    gui = GUI(cur_path)
    gui.start()
