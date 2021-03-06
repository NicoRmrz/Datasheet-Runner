import os
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QFile, QDate, QDir, QFileInfo
import statistics 

from Excell import Excel_Report

'''
Class: excelThread
	Worker thread to handle populating an excel sheet

Parameters: 
	QThread - inherits QThread attributes
'''
class excelThread(QThread):
	sendReportName = pyqtSignal(str, bool)
	sendOutput = pyqtSignal(str)

	'''
	Function: __init__
		Sets initial values
	'''	
	def __init__(self):
		QThread.__init__(self)
		self.reportPath = ""
		self.name = ""
		self.dataAnalyDIR = ""
		self.state = False
		self.DAstate = False
		self.datasheet_dict = {}
		self.excel = Excel_Report()
		self.protocolHeader = ["Section", "Min", "Max", "Unit",  "Value", "Result", "Comment"]
		self.equipmentHeader = ["Name", "Model", "ID", "Calibration ID", "Cal Due Date"]
		self.toolHeader = ["Name", "Version"]
		self.materialHeader = ["Name", "Serial Number", "Revision", "Firmware", "Software"]

	'''
	Function: setDataAnalysis
		Set worker thread to perform data analysis

	Parameters: 
	  	dataDIR - DIR of all reports for data analysis 
	  	DAstate - set state to start worker thread
	'''
	def setDataAnalysis(self, dataDIR, state):
		self.dataAnalyDIR = dataDIR
		self.DAstate = state

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

		# ---------- Excel Report ----------
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
				row = self.excel.addHeaderRow(row, 1, "Equipment", self.equipmentHeader)

				# add content
				for i in self.datasheet_dict['Equipment']:
					if (i.get('Name') != ""):
						self.excel.writeExcelEntry(i.get('Name'), row, 1)
						self.excel.writeExcelEntry(i.get('Model'), row, 2)
						self.excel.writeExcelEntry(i.get('ID'), row, 3)
						self.excel.writeExcelEntry(i.get('Cal ID'), row, 4)

						# color out of calibration equipment red
						if (i.get('Cal Due Date') != ""):
							date = QDate.fromString(i.get('Cal Due Date'), "MMM d, yyyy") 
							if (date < QDate.currentDate()):
								self.excel.colorCellFail(row, 5)

						self.excel.writeExcelEntry(i.get('Cal Due Date'), row, 5)
						row += 1
			row += 1

			# Tools section
			if (len(self.datasheet_dict.get('Tools')) > 0):

				# add header
				row = self.excel.addHeaderRow(row, 1, "Tools", self.toolHeader)

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
				row = self.excel.addHeaderRow(row, 1, "Materials", self.materialHeader)

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
			row = self.excel.addHeaderRow(row, 1, "Test Procedure", self.protocolHeader)

			# populate excel report
			for i in self.datasheet_dict["Procedure"]:
				self.excel.writeExcelEntry(i.get('Section'), row, 1)
				self.excel.writeExcelEntry(i.get('Min'), row, 2)
				self.excel.writeExcelEntry(i.get('Max'), row, 3)
				self.excel.writeExcelEntry(i.get('Unit'), row, 4)
				if (i.get('Value')== ""):
					self.excel.writeExcelEntry('N/A', row, 5)
				else:
					self.excel.writeExcelEntry(i.get('Value'), row, 5)
				self.excel.writeExcelEntry(i.get('Result'), row, 6)

				# color fails red
				if (i.get('Result') == 'F'):
					self.excel.colorCellFail(row, 6)
				self.excel.writeExcelEntry(i.get('Comment'), row, 7)
				row += 1

			row += 2

			# input last row
			self.excel.writeSignature(row)

			# save excel report/ emit error 
			try:
				reportname = self.excel.SaveSheet(openFile)
				self.sendReportName.emit(reportname, True)
				
			# error is sheet is opened by user and trying to save
			except PermissionError as e:
				self.sendReportName.emit("FAILED: Please Close Opened Excel Sheet", False)

			self.state = False

		# ---------- Data Analysis ----------
		if self.DAstate:
			# put reports in folder in a local list
			DataAnalysisDIR = QDir(self.dataAnalyDIR)
			reportList = DataAnalysisDIR.entryList(QDir.Files, QDir.Time)
			reportDataList = []

			# Start data analysis sheet
			outputSheetName = self.excel.startDataAnalysis(self.dataAnalyDIR)

			# get base name to not parse
			baseReportName = QFileInfo(outputSheetName)
			
			# iterate through each report and append result data dicts to a list
			for report in reportList:
				if (report.endswith('.xlsx') and report != baseReportName.baseName() + '.xlsx'):
					inputReport = self.dataAnalyDIR + '/' + report
					resultDict = self.excel.parseReport(inputReport)
					reportDataList.append(resultDict)

			# declare local variable for populating data analysis
			serNumList = []
			row = 3
			dataCol = 5
			numTests = len(reportDataList[0]["Section"])
			numReports = len(reportDataList)

			# add serial numbers in list for header
			for i in range(0, numReports):
				serNumList.append(reportDataList[i].get("Serial Number"))

			# write header to data analysis
			row = self.excel.addHeaderRow(row, dataCol, "Serial Numbers", serNumList)
			self.excel.addSingleHeader(row - 1, 4, "Unit")
			self.excel.addSingleHeader(row - 1, 3, "Max")
			self.excel.addSingleHeader(row - 1, 2, "Min")
			self.excel.addSingleHeader(row - 1, 1, "Section")

			# populate with report data
			for test in range(0, numReports):
				for i in range(0, numTests):
					self.excel.writeExcelEntry(reportDataList[test]["Section"][i], row + i, 1)
					self.excel.writeExcelEntry(reportDataList[test]["Min"][i], row + i, 2)
					self.excel.writeExcelEntry(reportDataList[test]["Max"][i], row + i, 3)
					self.excel.writeExcelEntry(reportDataList[test]["Unit"][i], row + i, 4)
					self.excel.writeExcelEntry(reportDataList[test]["Value"][i], row + i, dataCol + test)

					# color failed tests red
					if (reportDataList[test]["Result"][i] == "F"):
						self.excel.colorCellFail(row + i, dataCol + test)

			# add in Data Analysis columns
			stanDevCol 	= dataCol + numReports
			minCol 		= dataCol + numReports + 1
			maxCol		= dataCol + numReports + 2
			headerRow 	= row - 1
			currRow		= row
			testIndex 	= 0

			self.excel.addSingleHeader(headerRow, stanDevCol, "Standard Deviation")
			self.excel.addSingleHeader(headerRow, minCol, "Min")
			self.excel.addSingleHeader(headerRow, maxCol, "Max")

			# iterate all tests and get list of values of each test
			testDataList = self.excel.getTestDataList(numTests, numReports, currRow, dataCol)

			# perform analysis
			for test in testDataList:

				if ('N/A' in test):
					self.excel.writeExcelEntry("N/A", currRow, stanDevCol)
					self.excel.writeExcelEntry("N/A", currRow, minCol)
					self.excel.writeExcelEntry("N/A", currRow, maxCol)

				else:
					standardDeviation = statistics.stdev(testDataList[testIndex])
					minimumVal = min(testDataList[testIndex])
					maximumVal = max(testDataList[testIndex])
					self.excel.writeExcelEntry(standardDeviation, currRow, stanDevCol)
					self.excel.writeExcelEntry(minimumVal, currRow, minCol)
					self.excel.writeExcelEntry(maximumVal, currRow, maxCol)

				# increment current row and test index
				currRow += 1 
				testIndex += 1

			# get standard deviation column
			stanDevData = self.excel.getDataColumn(numTests, row, stanDevCol)


			print(stanDevData)



			# make bar graph --- UPDATE FUNCTION
			self.excel.createBarGraph(row, numTests, stanDevCol)

			# for i in range(0, numTests):
			# 	for test in range(0, numReports):
			# 		print("Test: " + str(test))
			# 		print("Result:  " + str(reportDataList[test]["Result"][i]))
			# 		print("Value:  " + str(reportDataList[test]["Value"][i]))

			# save data analysis sheet/ emit error 
			try:
				reportname = self.excel.SaveSheet(outputSheetName)
				self.sendOutput.emit("")
				self.sendOutput.emit("Data Analysis Successful!")
				self.sendOutput.emit("Saved As: " + reportname)

			# error is sheet is opened by user and trying to save
			except PermissionError as e:	
				self.sendOutput.emit("")
				self.sendOutput.emit("FAILED: Please Close Opened Excel Sheet")
				self.sendOutput.emit(str(e))

			self.DAstate = False