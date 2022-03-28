import numpy as np
import random
import math

class Generate:
	def __init__(self):
		self.dicoDroite = self.createDicoDroite()
		self.dicoGauche = self.createDicoGauche()
		self.count = 0
		self.count1 = 0

	def codebarreWithDigits(self, codeBarre):
		digits = {}
		for x, item in enumerate(codeBarre):
			digits[f"{x+1}"] = item
		code = self.translateCodeBar(digits)
		bonSens = random.randint(0,1)
		if bonSens:
			return code
		else:
			return code[::-1]

	def generateNumber(self):
		digits = {}
		digits["1"] = 0
		for i in range(10):
			number = str(i + 2)
			digits[number] = random.randint(0,9)
		return digits

	def generateModuloCheck(self, digits):
		oddDigits = (digits["1"]+digits["3"]+digits["5"]+digits["7"]+digits["9"]+digits["11"])
		evenDigits = (digits["2"]+digits["4"]+digits["6"]+digits["8"]+digits["10"])
		formula = 3*oddDigits+evenDigits
		upper10 = math.ceil(formula/10)*10
		moduloCheck = upper10 - formula
		return moduloCheck

	def codebarre(self):
		while True:
			digits = self.generateNumber()
			moduloCheck = self.generateModuloCheck(digits)
			digits["12"] = moduloCheck
			codeBarre = str(digits["1"])+str(digits["2"])+str(digits["3"])+str(digits["4"])+str(digits["5"])+str(digits["6"])+str(digits["7"])+str(digits["8"])+str(digits["9"])+str(digits["10"])+str(digits["11"])+str(moduloCheck)
			code = self.translateCodeBar(digits)
			countLeft = code[10:45].count("1")
			countRight = code[50:85].count("1")
			if countLeft %2 == 1:
				if countRight %2 == 0:
					break
		# return code
		bonSens = random.randint(0,1)
		self.count1 += 1
		if bonSens:
			return code
		else:
			self.count += 1
			return code[::-1]

	def translateCodeBar(self, digits):
		code = "101"
		code = code + self.dicoGauche[str(digits["1"])]
		code = code + self.dicoGauche[str(digits["2"])]
		code = code + self.dicoGauche[str(digits["3"])]
		code = code + self.dicoGauche[str(digits["4"])]
		code = code + self.dicoGauche[str(digits["5"])]
		code = code + self.dicoGauche[str(digits["6"])]
		code = code + "01010"
		code = code + self.dicoDroite[str(digits["7"])]
		code = code + self.dicoDroite[str(digits["8"])]
		code = code + self.dicoDroite[str(digits["9"])]
		code = code + self.dicoDroite[str(digits["10"])]
		code = code + self.dicoDroite[str(digits["11"])]
		code = code + self.dicoDroite[str(digits["12"])]
		code = code + "101"
		return code

	def randomNumber(self):
		return str(random.randint(1,4))

	def createDicoGauche(self):
		dicoGauche = {}
		dicoGauche["0"] = "0001101"
		dicoGauche["1"] = "0011001"
		dicoGauche["2"] = "0010011"
		dicoGauche["3"] = "0111101"
		dicoGauche["4"] = "0100011"
		dicoGauche["5"] = "0110001"
		dicoGauche["6"] = "0101111"
		dicoGauche["7"] = "0111011"
		dicoGauche["8"] = "0110111"
		dicoGauche["9"] = "0001011"
		return dicoGauche

	def createDicoDroite(self):
		dicoDroite = {}
		dicoDroite["0"] = "1110010"
		dicoDroite["1"] = "1100110"
		dicoDroite["2"] = "1101100"
		dicoDroite["3"] = "1000010"
		dicoDroite["4"] = "1011100"
		dicoDroite["5"] = "1001110"
		dicoDroite["6"] = "1010000"
		dicoDroite["7"] = "1000100"
		dicoDroite["8"] = "1001000"
		dicoDroite["9"] = "1110100"
		return dicoDroite
