from PyQt5.QtCore import pyqtSignal, QThread, QMutex, Qt, QSize, QTimer
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QPixmap
from PyQt5 import uic
from tools.ThreadWorker import Worker
from Model.Fakeduino import Fakeduino
from Model import Analyse
from Model import dataBase
from datetime import datetime
import winsound
import serial
import time
import os

frequency = 2500 #Hz
duration = 150

def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()

applicationPath = os.path.abspath("")
MainWindowPath = os.path.dirname(os.path.realpath(__file__)) + '{0}ui{0}ScanWindow.ui'.format(os.sep)
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainWindowPath)

class ViewScan(QWidget, Ui_MainWindow):

    threadSignalFinished = pyqtSignal(int)
    findSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.analyse = Analyse()
        self.initializeArduino()
        self.dico = dataBase.extractInfos()
        self.total = 0
        self.code = ""
        self.data = []
        self.typing = False
        self.facture = {}
        self.priceList = {}
        self.connectWidgets()
        self.initializeButtons()
        self.showInfos(True, True)
        self.threadRelated()

    def connectWidgets(self):
        self.pb_scan.clicked.connect(self.startThread)
        self.pb_resetTotal.clicked.connect(self.resetFacture)
        self.pb_validate.pressed.connect(self.changeTypingStatus)
        self.threadSignalFinished.connect(self.killThread)
        self.findSignal.connect(self.findCode)
        self.pb_0.pressed.connect(self.typingCode)
        self.pb_1.pressed.connect(self.typingCode)
        self.pb_2.pressed.connect(self.typingCode)
        self.pb_3.pressed.connect(self.typingCode)
        self.pb_4.pressed.connect(self.typingCode)
        self.pb_5.pressed.connect(self.typingCode)
        self.pb_6.pressed.connect(self.typingCode)
        self.pb_7.pressed.connect(self.typingCode)
        self.pb_8.pressed.connect(self.typingCode)
        self.pb_9.pressed.connect(self.typingCode)
        self.pb_delete.pressed.connect(self.deleteCode)

    def deleteCode(self):
        self.code = ""
        self.showInfos(self.code, initialize=True)
        self.typing = False

    def analyseCode(self):
        separator = 2
        lastCode = ""
        lastTime = 0
        code = None
        count = 0
        while True:
            byte = self.arduino.readline()
            try:
                byte = byte.strip()
                value = int.from_bytes(byte,'little')
                if (value != 0) and (value!=1):
                    if value == separator and len(self.data) > 1000:
                        if count > 5:
                            code = Analyse.analyse(self.data[1:len(self.data)])
                            if code != "":
                                if code is not None:
                                    if code != lastCode:
                                        self.findSignal.emit(code)
                                        lastCode = code
                                        lastTime = time.perf_counter()
                            if time.perf_counter() > 2 + lastTime:
                                lastCode = ""
                            self.data = []
                            count = 1
                        else:
                            count += 1        
                    else:
                        self.data = []
            except Exception as e:
                pass
            if value != separator:
                self.data.append(value)
            self.mutex.lock()
            if self.stopThread == True:
                self.mutex.unlock()
                break
            self.mutex.unlock()
        self.threadSignalFinished.emit(0)

    def findCode(self, code):
        self.showInfos(code)

    def typingCode(self):
        sender = self.sender().text()
        if not self.typing:
            return None
        self.code += sender
        code = self.code

        if len(self.code) == 12:
            code = self.code
            self.code = ""
            self.showInfos(code)
        else:
            self.showInfos(code, typing=True)

    def changeTypingStatus(self):
        if self.typing:
            self.typing = False
        else:
            self.typing = True

    def showInfos(self, code, initialize=False, typing=False):
        if initialize:
            self.te_affichage.clear()
            self.te_affichage.append(f"Nom: ")
            self.te_affichage.append(f"Prix: ")
            self.te_affichage.append(f"")
            self.te_affichage.append(f"")
            self.te_affichage.append(f"Total: {round(self.total,2)} $")
            return None

        if typing:
            self.te_affichage.clear()
            self.te_affichage.append(f"Code: {code}")
            self.te_affichage.append(f"Prix: N/D")
            self.te_affichage.append(f"")
            self.te_affichage.append(f"")
            self.te_affichage.append(f"Total: {round(self.total,2)} $")
            return None

        try:
            data = self.dico[code]
            if data == None:
                return None
            self.te_affichage.clear()
            itemName = data[0]
            price = data[1]
            self.total += price
            total = round(self.total, 2)
            self.te_affichage.append(f"Nom: {itemName}")
            self.te_affichage.append(f"Prix: {price} $")
            self.te_affichage.append(f"")
            self.te_affichage.append(f"")
            self.te_affichage.append(f"Total: {total} $")
            self.typing = False
            winsound.Beep(frequency, duration)
            self.updateFacture(itemName, price)
        except Exception as e:
            self.te_affichage.clear()
            self.te_affichage.append(f"Nom: INVALID NUMBER")
            self.te_affichage.append(f"Prix: N/D")
            self.te_affichage.append(f"")
            self.te_affichage.append(f"")
            self.te_affichage.append(f"Total: {round(self.total,2)} $")
            self.typing = False

    def updateFacture(self, itemName, price):
        if itemName in list(self.facture.keys()):
            self.facture[itemName] += 1
        else:
            self.facture[itemName] = 1
            self.priceList[itemName] = price
        self.showFacture()

    def showFacture(self):
        self.te_facture.clear()
        self.te_facture.append("                   UNIVERSITÉ LAVAL")
        self.te_facture.append("               2325 RUE DE L'UNIVERSITÉ")
        self.te_facture.append("                        QUEBEC      ")
        self.te_facture.append("                        G1V 0A6")
        self.te_facture.append("")
        now = datetime.now()
        currentDate = now.strftime("%Y-%m-%d")
        currentTime = now.strftime("%H:%M:%S")
        text = f"DATE:    {currentDate}sPaCerHeure:    {currentTime}"
        nbSpace = 54 - len(text) + 6
        text = text.replace("sPaCer", nbSpace*" ")
        self.te_facture.append(text)
        self.te_facture.append("")
        self.te_facture.append(f"    ----------------------------------------------    ")
        self.te_facture.append("")
        for itemName in list(self.facture.keys()):
            qty = self.facture[itemName]
            price = self.priceList[itemName]
            qtyPrice = str(round(qty*price, 2))
            if len(qtyPrice) < 8:
                nbSpace = 8 - len(qtyPrice)
                qtyPrice = nbSpace*" " + qtyPrice
            text = f"{itemName}sPaCer{qty}{qtyPrice}$"
            nbSpace = 54 - len(text) + 6
            if nbSpace < 2:
                self.te_facture.append(f"{itemName}")
                end = f"{qty}{qtyPrice}$"
                nbSpace =  54 - len(end)
                text = nbSpace*" " + f"{qty}{qtyPrice}$"
            elif nbSpace%2 == 0:
                text = text.replace("sPaCer", int(nbSpace)*" ")
            else:
                text = text.replace("sPaCer", int(nbSpace)*" ")
            self.te_facture.append(text)
            self.te_facture.append("")
        self.te_facture.append("")
        self.te_facture.append(f"    ----------------------------------------------    ")
        self.te_facture.append(f"           TOTAL   CAN   $ {round(self.total, 2)}")
        self.te_facture.append(f"    ----------------------------------------------    ")

    def resetFacture(self):
        self.total = 0
        self.showInfos("code", initialize=True)
        self.facture = {}
        self.priceList = {}
        self.te_facture.clear()

    def setIconsImage(self, pb, image, imageSelected):
        pb.setIcons(QPixmap(image).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation),
                                QPixmap(imageSelected).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def imagesPath(self):
        folder = applicationPath + "/View/icons/"
        folderList = {"0": "0", "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "delete": "delete", "#": "hastag"}
        images = {}
        for i in list(folderList.keys()):
            name = folderList[i]
            images[f"{i}"] = (folder + f"{name}.png", folder + f"{name}_selected.png")
        return images

    def initializeButtons(self):
        buttonsList = {"0": self.pb_0, "1": self.pb_1, "2": self.pb_2, "3": self.pb_3, "4": self.pb_4, "5": self.pb_5, "6": self.pb_6, "7": self.pb_7, "8": self.pb_8, "9": self.pb_9, "delete": self.pb_delete, "#": self.pb_validate}
        images = self.imagesPath()
        for i in list(buttonsList.keys()):
            pb = buttonsList[i]
            filePath = images[i]
            image = filePath[0]
            imageSelected = filePath[1]
            self.setIconsImage(pb, image, imageSelected)

    def initializeArduino(self):
        try:
            self.arduino = serial.Serial("COM3", baudrate = 1000000, timeout = 0.1)
            if self.arduino.isOpen():
                self.connected = True
            else:
                self.connected = False
                self.arduino = Fakeduino()
        except:
            self.connected = False
            self.arduino = Fakeduino()

    #Thread

    def threadRelated(self):
        self.stopThread = True
        self.mutex = QMutex()
        self.analyseWorker = Worker(self.analyseCode)
        self.analyseThread = QThread()
        self.createThreads()

    def startThread(self):
        self.startAnalyseThread()
        try:
            self.consoleView.showOnConsole(consoleStr[0], consoleStr[1])
        except:
            pass

    def startAnalyseThread(self):
        threadRunning = self.analyseThread.isRunning()
        if threadRunning == False:
            self.mutex.lock()
            self.stopThread = False
            self.mutex.unlock()
            self.analyseThread.start()
            self.consoleView.showOnConsole("Start Analyse Thread", "green")
        else:
            self.stopAnalyseThread()
            self.consoleView.showOnConsole("Press again on start (ThreadKilled)", "red")

    def stopAnalyseThread(self):
        self.mutex.lock()
        self.stopThread = True
        self.mutex.unlock()

    def createThreads(self):
        self.analyseWorker.moveToThread(self.analyseThread)
        self.analyseThread.started.connect(self.analyseWorker.run)

    def killThread(self, ID):
        self.analyseThread.quit()
