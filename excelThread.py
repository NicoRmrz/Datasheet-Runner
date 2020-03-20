import os
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QFile

from Excell import Excel_Report

'''
Class: excelThread
	Worker thread to handle populating an excel sheet

Parameters: 
	QThread - inherits QThread attributes
'''
class excelThread(QThread):
	sendReportName = pyqtSignal(str)

	'''
	Function: __init__
		Sets initial values
	'''	
	def __init__(self):
		QThread.__init__(self)
		self.reportPath = ""
		self.name = ""
		self.state = False
		self.datasheet_dict = {}
		self.excel = Excel_Report()

	'''
	Function: setGenerateExcel
		Set worker thread to generate excel file

	Parameters: 
	  	outputDict - output dictionary to populate excel report 
	  	exportPath - report export network path
	  	reportName - name for report
	  	state 	   - set state to start worker thread
	'''
	def setGenerateExcel(self, outputDict, exportPath, reportName, state):
		self.datasheet_dict = outputDict
		self.reportPath = exportPath
		self.name = reportName
		self.state = state
		
	'''
	Function: run
		This function is started by.start() and runs the main portion of the code
	'''
	def run(self):
		self.setPriority(QThread.HighestPriority)

		if self.state:
			# create excel sheet and set header
			openFile = self.excel.startExcelSheet(	self.reportPath, 
													self.name, 
													self.datasheet_dict.get('Serial Number'), 
													self.datasheet_dict.get('Protocol Name'))
			
			# row to start populating data
			row = 4

			# populate excel report
			for i in self.datasheet_dict["Procedure"]:
				self.excel.writeExcelEntry(i.get('Section'), row, 1)
				self.excel.writeExcelEntry(i.get('Min'), row, 2)
				self.excel.writeExcelEntry(i.get('Max'), row, 3)
				self.excel.writeExcelEntry(i.get('Unit'), row, 4)
				self.excel.writeExcelEntry(i.get('Value'), row, 5)
				self.excel.writeExcelEntry(i.get('Result'), row, 6)

				# color fails red
				if (i.get('Result') == 'F'):
					self.excel.colorCellFail(row, 6)
				self.excel.writeExcelEntry(i.get('Comment'), row, 7)
				row += 1

			# save excel report
			reportname = self.excel.SaveSheet(openFile)
			self.sendReportName.emit(reportname)

			self.state = False
