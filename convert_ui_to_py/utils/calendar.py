# Form implementation generated from reading ui file 'UI/calendar.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from pathlib import Path


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 100)
        MainWindow.setMinimumSize(QtCore.QSize(300, 100))
        MainWindow.setMaximumSize(QtCore.QSize(300, 100))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 10, 191, 31))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 55, 80, 30))
        self.pushButton.setObjectName("pushButton")

        # file selection
        self.file_browser_btn = QtWidgets.QPushButton(
            parent=self.centralwidget)
        self.file_browser_btn.setObjectName("browseButton")
        self.file_browser_btn.clicked.connect(self.open_file_dialog)
        # layout.addWidget(self.button)

        self.filename_edit = QtWidgets.QLineEdit()

        # layout.addWidget(QLabel('Files:'), 0, 0)
        # layout.addWidget(self.file_list, 1, 0)
        # layout.addWidget(file_browser_btn, 2, 0)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate(
            "MainWindow", "Đã qua [] từ phase 2 phiên bản []"))
        self.pushButton.setText(_translate("MainWindow", "OK"))
        self.file_browser_btn.setText(_translate("MainWindow", "Browse"))

    def open_file_dialog(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "All Files (*);;Text Files (*.txt)"
        )
        if file_name:
            print(f"Selected file: {file_name}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
