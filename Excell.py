from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, colors, PatternFill, Color, Font
from openpyxl.styles.borders import Border, Side
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string, get_column_letter
import openpyxl
import time
import datetime
import os
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize

'''
Class: Excel_Report
    Class to handle all excel file generation functions
    
Parameters: 
    QObject - inherits QObject attributes
'''
class Excel_Report(QObject):
    suffix = "_Report"
    path = ""
    reportExport = ""

    '''
    Function: __init__
		  initializes when class is called
    '''
    def __init__(self):
        self.thick_border = Side(border_style = "thick")
        self.thin_border = Side(border_style= 'thin')
        self.THICK =  Border( top=self.thick_border,left=self.thick_border, right=self.thick_border,bottom=self.thick_border)
        self.THIN = Border(top = None, left = self.thin_border, right = self.thin_border,bottom = self.thin_border)
        self.fontStyle = Font(size = "14")
        self.largeFontStyle = Font(size = "20",bold=True)
        self.boldFont = Font(size = "14",bold=True)
        self.fillColor = PatternFill(fgColor=Color('CDCDCD'), fill_type = "solid")
        self.centerAlignment = Alignment( horizontal='center', vertical='center', wrap_text=True)

    '''
    Function: startExcelSheet
		  Create excel report sheet and set heading

    Parameters: 
	  	exportPath - report export network path
	  	name       - input JSON file name
	  	serialNum  - serial number of DUT
	  	Protocol   - Protocol name from JSON file

    Returns: 
	  	openFileName - current open excel file
    '''
    def startExcelSheet(self, exportPath, name, serialNum, Protocol):

        self.path = exportPath + name+ "/"

        #Create test folder path in report folder
        if not os.path.exists(self.path):
          os.makedirs(self.path)

        self.suffix = serialNum + self.suffix
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = serialNum

        # Write protocol name on header
        report = self.ws.cell(row=1, column=1)
        report.fill =  self.fillColor
        report.font  =  self.fontStyle
        report.value = "Test Report: " 
        report.border = self.THICK 

        # Write protocol name on header
        self.ws.merge_cells("B1:C1")
        report = self.ws["B1"]
        report1 = self.ws["C1"]
        report.fill =  self.fillColor
        report.font  =  self.boldFont
        report.value = Protocol 
        report.border = self.THICK 
        report1.border = self.THICK 
        report.alignment = self.centerAlignment

        # Write serial number name on header
        serNum = self.ws.cell(row=2, column=1)
        serNum.fill =  self.fillColor
        serNum.font  =  self.fontStyle
        serNum.value = "Serial Number: "
        serNum.border = self.THICK 

        # Write serial number name on header
        self.ws.merge_cells("B2:C2")
        serNum = self.ws["B2"]
        serNum1 = self.ws["C2"]
        serNum.fill =  self.fillColor
        serNum.font  =  self.boldFont
        serNum.value = serialNum
        serNum.border = self.THICK 
        serNum1.border =  self.THICK 
        serNum.alignment = self.centerAlignment

        openFileName = self.path + self.suffix
        return openFileName

    '''
    Function: addHeaderRow
        Create excel sheet section heading

    Parameters: 
	  	Hrow         - row to enter header
	  	title        - section  header title
	  	headerList   - items to put on header row

    Return:
        next row
    '''
    def addHeaderRow(self, Hrow, title, headerList):
        # Create header title
        headerLen = len(headerList)
        self.ws.merge_cells(start_row=Hrow, start_column=1, end_row=Hrow, end_column=headerLen)
        titleCell =  self.ws.cell(row=Hrow, column=1)
        titleCell.value = title
        titleCell.font  =  self.boldFont
        titleCell.fill =  self.fillColor
        titleCell.alignment = self.centerAlignment

        # Next Row
        Hrow += 1

        # write in header
        headCol = 1
        for i in headerList:
            self.ws.cell(row=Hrow, column=headCol).value = i

            # Border cell
            self.ws.cell(row=Hrow-1, column=headCol).border = self.THICK # add border to header title
            self.ws.cell(row=Hrow, column=headCol).border = self.THIN 
                                                        
            # Align cell
            self.ws.cell(row=Hrow, column=headCol).alignment = self.centerAlignment

            # color header
            self.ws.cell(row=Hrow, column=headCol).fill =  self.fillColor                                                            
            headCol += 1
        
        Hrow += 1
        return Hrow

    '''
    Function: writeExcelEntry
		  Writes to excel sheet

    Parameters: 
	  	entry - value to write to excel sheet
	  	row - excel row to write to 
	  	col - excel col to write to 
    '''
    def writeExcelEntry(self, entry, row, col):
        enterCell = self.ws.cell(row=row, column=col)
        enterCell.value = entry

        # Align cell
        self.ws.cell(row, col).alignment = self.centerAlignment

        # create border per cell
        enterCell.border = self.THIN

    '''
    Function: colorCellFail
		  Color Fails test Cell Red

    Parameters: 
	  	row - excel row 
	  	col - excel col 
    '''
    def colorCellFail(self, row, col):
        colorCell = self.ws.cell(row=row, column=col)
        fillColor = PatternFill(fgColor=colors.RED, fill_type = "solid")
        colorCell.fill = fillColor

    '''
    Function: startDataAnalysis
        Create excel data analysis sheet and set heading

    Parameters: 
	  	reportPath - path to export data analysis when finished
    
    Returns: 
	  	DAfileName - name of data analysis sheet
    '''
    def startDataAnalysis(self, reportPath):
        self.reportExport = reportPath
        DAfileName =  self.reportExport + "/Data_Analysis_Results"

        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = "Data Analysis"
        self.ws.merge_cells("A1:C1")

        # Write data analysis name on header
        DAHeader = self.ws.cell(row=1, column=1)
        DAHeader.fill =  self.fillColor
        DAHeader.font  =  self.largeFontStyle
        DAHeader.value = "Data Analysis" 
        DAHeader.border = self.THICK 
        self.ws.cell(row=1, column=2).border = self.THICK 
        self.ws.cell(row=1, column=3).border = self.THICK 

        return DAfileName

    '''
    Function: parseReport
        parse input report and retreive all data

    Parameters: 
	  	inputReport - input report to parse data
    
    Returns: 
	  	resultDict - dictionary of results from report
    '''
    def parseReport(self, inputReport):
        print(inputReport)
        resultDict =[]

        return resultDict

    '''
    Function: getTimestamp
		  Gets current time for timestamp

    Returns: 
	  	timestamp_return - current timestamp
    '''
    def getTimestamp(self):
        timestamp_return = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H_%M_%S')
        return timestamp_return

    '''
    Function: SaveSheet
		  To save excel report with timestamp

    Parameters: 
	  	fileToSave - open file to save

    Returns: 
	  	Final_Report_Name - report name to display on UI
    '''
    def SaveSheet(self, fileToSave):
        # To Auto Fit column width
        dims = {}
        for row in self.ws.rows:
            for cell in row:
                if cell.value:
                    dims[cell.column] = max((dims.get(cell.column, 0), len(str(cell.value))))
                     
        for col, value in dims.items():
            # print (str(col) + ", " + str(value))
            self.ws.column_dimensions[col].width = value+3
            # self.ws.column_dimensions[get_column_letter(col)].width = value+3

        #Timestamps the file
        # gettime = self.getTimestamp()
        # Final_Report_Name = fileToSave + gettime + '.xlsx'
        Final_Report_Name = fileToSave + '.xlsx'
        self.wb.save(Final_Report_Name)

        self.suffix = "_Report"

        return Final_Report_Name
