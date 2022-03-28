import random
from Model.Barcode import Generate
from Model import dataBase
import time

class Fakeduino:
    def __init__(self):
        self.count = 0
        self.data = ReadableData().data

    def close(self):
        pass

    def readline(self):
        sleep(1.5e-5)
        self.count += 1
        try:
            readData = self.data[self.count]
        except:
            self.count = 0
            readData = self.data[self.count]

        if readData == "0":
            return b'\x01'
        elif readData == "1":
            return b'\x00'
        elif readData == "2":
            return b'\x02'
        else:
            print("error")

class ReadableData:
    def __init__(self):
        self.generate = Generate()
        self.dataBase = dataBase.extractInfos()
        self.data = self.createRandomData()

    def createRandomData(self):
        data = ""
        for i in range(100):
            luck = random.random()
            if luck > 0.8:
                indice = random.randint(0, len(list(self.dataBase.keys())))
                liste = list(self.dataBase.keys())
                codebarre = liste[indice]
                code = self.generate.codebarreWithDigits(codebarre)
            else:
                code = ""
                for i in range(random.randint(0,9)):
                    code += str(random.randint(0,1))

            longueur = 4096 - len(code)
            if longueur%2 == 1:
                len1 = int(longueur/2)
                len2 = int(longueur/2) + 1
            if longueur%2 == 0:
                len1 = int(longueur/2)
                len2 = int(longueur/2)

            data += "2" + len1*"0" + code + len2*"0"
        return list(data)

def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()