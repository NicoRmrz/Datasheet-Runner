import os
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QFile

from scriptParser import scriptParser

  # Class: parserThread
#       Worker thread to handle all the parsing of the input scripts
# Parameters: 
#       QThread - inherits QThread attributes
class parserThread(QThread):
	inputScript = ""
	parseState = False
	success = False

	def __init__(self):
		QThread.__init__(self)
		self.parser = scriptParser()

	def setScriptToParse(self, pathToFile, state):
		self.inputScript = pathToFile
		self.parseState = state
		
	def run(self):
		self.setPriority(QThread.HighestPriority)

		if self.parseState:
		    success = self.parser.parseScriptFile(self.inputScript)
		    parseState = False
			
					
