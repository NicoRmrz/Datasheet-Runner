import os
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QFile

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
		print(pathToFile)

		success = True
		return success

