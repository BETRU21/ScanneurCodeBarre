from pyzbar.pyzbar import decode

def analyse(data):
	byteDatas = bytes([i * 255 for i in data])
	barcode = decode((byteDatas * 15, len(byteDatas), 15))
	encodedInfos = ''
	codeBarre = ''
	if barcode:
		encodedInfos = barcode[0][0].decode('utf-8')
		for index in range(1, 13):
			codeBarre += str(encodedInfos)[index]
		if len(codeBarre) > 12:
			codeBarre = codeBarre[1:]
	return  codeBarre
	