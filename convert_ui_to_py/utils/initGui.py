from PyQt6 import QtWidgets
from utils.mainWindow import Ui_MainWindow
import sys


class CaldendarWindow():
    def __init__(self, path):
        self.closed = False

        self.path = path
        self.app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)

    def init_main_window(self):
        # Init statusBar
        self.ui.statusBar = QtWidgets.QStatusBar(self.MainWindow)
        self.ui.statusBar.setObjectName("Statfus bar")
        self.MainWindow.setStatusBar(self.ui.statusBar)
        self.ui.statusBar.hide()
        self.ui.statusBar.setStyleSheet('color: #000; background-color: #fff')

        # Signals
        # self.ui.file_browse.clicked.connect(self.open_file_dialog)


    # Choose file
    def open_file_dialog(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.MainWindow,
            "Open File",
            "",
            "All Files (*);;Text Files (*.txt)"
        )
        if file_name:
            print(f"Selected file: {file_name}")


    # Drag and drop file
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)



    def end_program(self):
        self.closed = True

    def start(self):
        self.init_main_window()
        self.MainWindow.show()
        self.app.aboutToQuit.connect(self.end_program)
        sys.exit(self.app.exec())
