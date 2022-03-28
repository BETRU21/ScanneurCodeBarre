from PyQt5.QtWidgets import QMainWindow, QTabWidget, QAction, QLabel, QMenu
from View.ViewConsole import ViewConsole
from View.ViewScan import ViewScan
from PyQt5 import uic
import os

MainWindowPath = os.path.dirname(os.path.realpath(__file__)) + '{0}ui{0}MainWindow.ui'.format(os.sep)
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainWindowPath)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.createsComponentsAndPointers()
        self.setupWindowTabs()

    def setupWindowTabs(self):
        self.tabWidget = QTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.tabWidget.addTab(self.scanView, "Scan")
        self.tabWidget.addTab(self.consoleView, "Console")

    def createsComponentsAndPointers(self):
        # Components
        self.scanView = ViewScan()
        self.consoleView = ViewConsole()
        # Pointers
        self.scanView.consoleView = self.consoleView
        self.consoleView.scanView = self.scanView
        if self.scanView.connected:
            self.consoleView.showOnConsole("Arduino connected", "green")
        else:
            self.consoleView.showOnConsole("No arduino connected, Initialize Fakeduino", "red")
