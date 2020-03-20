import os
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QFile
import json

'''
Class: parserThread
	Worker thread to handle all the parsing of the input scripts

Parameters: 
	QThread - inherits QThread attributes
'''
class parserThread(QThread):
	sendOutput = pyqtSignal(str)
	sendDict = pyqtSignal()

	'''
	Function: __init__
		Sets initial values
	'''
	def __init__(self):
		QThread.__init__(self)
		self.inputScript = ""
		self.parseState = False
		self.datasheet_dict = {}
		self.success = False

	'''
	Function: setScriptToParse
		Set worker thread to read in JSON file

	Parameters: 
	  	pathToFile - input file path
	  	state - set state to start worker thread
	'''
	def setScriptToParse(self, pathToFile, state):
		self.inputScript = pathToFile
		self.parseState = state
		
	'''
	Function: run
		This function is started by.start() and runs the main portion of the code
	'''
	def run(self):
		self.setPriority(QThread.HighestPriority)

		if self.parseState:
			self.datasheet_dict.clear()
			try:								 
				# Open Valid JSON script and store in dict
				with open(self.inputScript, 'r') as f:
					self.datasheet_dict = json.load(f)

			#Send errors if any
			except json.decoder.JSONDecodeError as e:
				self.success = False
				self.sendOutput.emit("Failed To Parse File")
				self.sendOutput.emit(str(e))

			# send mainWindow Dict is ready
			finally:
				if (len(self.datasheet_dict) > 0):
					self.success = True
					self.sendDict.emit()
					
			self.parseState = False

	'''
	Function: getDict
		Get dictionary to mainWindow
		
	Returns: 
		python dictionary of input JSON file
	'''
	def getDict(self):
		return self.datasheet_dict
