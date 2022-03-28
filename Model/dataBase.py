import os

splitSymbol = ","
path = os.path.abspath("") + "{0}PriceList{0}".format(os.sep)
maxLen=None

def extractInfos():
	try:
		fich = open(path + "upcPrice.txt", "r", encoding="Latin-1")
	except:
		fich = open(path + "upcPriceMinimal.txt", "r", encoding="Latin-1")
	if maxLen == None:
		fichStr = list(fich)
	else:
		fichStr = list(fich)[:maxLen]
	fich.close()

	data = {}
	for i in fichStr:
		elemStr = i.replace("\n", "")
		if elemStr[:2] == "00":
			elem = elemStr.split(splitSymbol)
			code = elem[0][1:]
			potentialName1 = elem[-2]
			potentialName2 = elem[-3]

			price = elem[-1]
			try:
				potentialName1 = int(potentialName1)
				articleName = potentialName2
			except:
				articleName = potentialName1
			try:
				data[f"{code}"] = (articleName, float(price))
			except:
				data[f"{code}"] = (articleName, "indeterminé")
	return data
