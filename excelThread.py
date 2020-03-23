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
		self.protocolHeader = ["Section", "Min", "Max", "Unit",  "Value", "Result", "Comment"]
		self.equipmentHeader = ["Name", "Model", "ID", "Calibration ID", "Cal Due Date"]
		self.toolHeader = ["Name", "Version"]
		self.materialHeader = ["Name", "Serial Number", "Revision", "Firmware", "Software"]


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

			# Equipment Used section
			if (len(self.datasheet_dict.get('Equipment')) > 0):
				
				# add header
				row = self.excel.addHeaderRow(row, "Equipment", self.equipmentHeader)

				# add content
				for i in self.datasheet_dict['Equipment']:
					if (i.get('Name') != ""):
						self.excel.writeExcelEntry(i.get('Name'), row, 1)
						self.excel.writeExcelEntry(i.get('Model'), row, 2)
						self.excel.writeExcelEntry(i.get('ID'), row, 3)
						self.excel.writeExcelEntry(i.get('Cal ID'), row, 4)
						self.excel.writeExcelEntry(i.get('Cal Due Date'), row, 5)
						row += 1
			row += 1

			# Tools section
			if (len(self.datasheet_dict.get('Tools')) > 0):

				# add header
				row = self.excel.addHeaderRow(row, "Tools", self.toolHeader)

				# add content
				for i in self.datasheet_dict['Tools']:
					if (i.get('Name') != ""):
						self.excel.writeExcelEntry(i.get('Name'), row, 1)
						self.excel.writeExcelEntry(i.get('Version'), row, 2)
						row += 1
			row += 1

			# Materials section
			if (len(self.datasheet_dict.get('Material')) > 0):

				# add header
				row = self.excel.addHeaderRow(row, "Materials", self.materialHeader)

				# add content
				for i in self.datasheet_dict['Material']:
					if (i.get('Name') != ""):
						self.excel.writeExcelEntry(i.get('Name'), row, 1)
						self.excel.writeExcelEntry(i.get('Serial Number'), row, 2)
						self.excel.writeExcelEntry(i.get('Revision'), row, 3)
						self.excel.writeExcelEntry(i.get('Firmware'), row, 4)
						self.excel.writeExcelEntry(i.get('Software'), row, 5)
						row += 1
			row += 1

			# write protocol header
			row = self.excel.addHeaderRow(row, "Test Procedure", self.protocolHeader)

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
