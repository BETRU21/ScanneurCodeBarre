from PyQt5.QtWidgets import QApplication, QMainWindow
from View.mainWindow import MainWindow as Window
from PyQt5.QtGui import QIcon
import ctypes
import sys
import os

if sys.platform == "win32":
    myappid = u"CodeScanner-version-1.0"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
else:
    pass

applicationPath = os.path.abspath("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Window()
    win.setWindowIcon(QIcon(applicationPath + "{0}View{0}logo{0}logo.ico".format(os.sep)))
    win.setWindowTitle("Scan")
    win.show()
    sys.exit(app.exec_())
