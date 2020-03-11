import os
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QFile
import json


  # Class: scriptParser
#       Functions to parse input script
# Parameters: 
#       QObject - inherits QObject attributes
class scriptParser(QObject):

	def __init__(self):
		QObject.__init__(self)

	def parseScriptFile(self, pathToFile):
		success = False
		Script = QFile(pathToFile)

		with open(pathToFile, 'r') as f:
			datasheet_dict = json.load(f)

		for distro in datasheet_dict:
			print(distro['Name'])

		with open('test/outdata.txt', 'w') as outfile:
			json.dump(datasheet_dict, outfile)

		success = True
		return success

