from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, colors, PatternFill, Color, Font
from openpyxl.styles.borders import Border, Side
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string, get_column_letter
import openpyxl
import time
import datetime
import os
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize, QElapsedTimer

'''
Class: Excel_Report
    Class to handle all excel file generation functions
    
Parameters: 
    QObject - inherits QObject attributes
'''
class Excel_Report(QObject):
    suffix = "_Report_"
    path = ""

    '''
    Function: __init__
		  initializes when class is called
    '''
    def __init__(self):
        self.thick_border = Side(border_style = "thick")
        self.thin_border = Side(border_style= 'thin')

    '''
    Function: startExcelSheet
		  Create excel sheet and set heading

    Parameters: 
	  	exportPath - report export network path
	  	name       - input JSON file name
	  	serialNum  - serial number of DUT
	  	Protocol   - Protocol name from JSON file

    Returns: 
	  	openFileName - current open excel file
    '''
    def startExcelSheet(self, exportPath, name, serialNum, Protocol):
        fontStyle = Font(size = "14")
        boldFont = Font(size = "14",bold=True)
        fillColor = PatternFill(fgColor=Color('CDCDCD'), fill_type = "solid")

        self.path = exportPath + name+ "/"

        #Create test folder path in report folder
        if not os.path.exists(self.path):
          os.makedirs(self.path)

        self.suffix = serialNum + self.suffix
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = serialNum

        # freeze header rows 
        self.ws.freeze_panes = self.ws['B4']

        # Write protocol name on header
        report = self.ws.cell(row=1, column=1)
        report.fill = fillColor
        report.font  = fontStyle
        report.value = "Test Report: " 
        report.border = Border( top=self.thick_border,left=self.thick_border, 
                                right=self.thick_border,bottom=self.thick_border)

        # Write protocol name on header
        report = self.ws.cell(row=1, column=2)
        report.fill = fillColor
        report.font  = boldFont
        report.value = Protocol 
        report.border = Border( top=self.thick_border,left=self.thick_border, 
                                right=self.thick_border,bottom=self.thick_border)
        report.alignment = Alignment( horizontal='center', vertical='center', wrap_text=True)

        # Write serial number name on header
        serNum = self.ws.cell(row=2, column=1)
        serNum.fill = fillColor
        serNum.font  = fontStyle
        serNum.value = "Serial Number: "
        serNum.border = Border( top=self.thick_border,left=self.thick_border, 
                                right=self.thick_border,bottom=self.thick_border)

        # Write serial number name on header
        serNum = self.ws.cell(row=2, column=2)
        serNum.fill = fillColor
        serNum.font  = boldFont
        serNum.value = serialNum
        serNum.border = Border( top=self.thick_border,left=self.thick_border, 
                                right=self.thick_border, bottom=self.thick_border)
        serNum.alignment = Alignment(  horizontal='center', vertical='center', wrap_text=True)

        # merge cells for input protocol name and serial number
        self.ws.merge_cells("B1:C1")
        self.ws.merge_cells("B2:C2")

        # write in header
        header = ["Section", "Min", "Max", "Unit",  "Value", "Result", "Comment"]
        headCol = 1
        for i in header:
            self.ws.cell(row=3, column=headCol).value = i

            # Border cell
            self.ws.cell(row=3, column=headCol).border = Border(top=self.thick_border,left=self.thick_border, 
                                                                right=self.thick_border,bottom=self.thick_border)
                                                        
            # Align cell
            self.ws.cell(row=3, column=headCol).alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

            # color header
            self.ws.cell(row=3, column=headCol).fill = fillColor                                                            
            headCol += 1

        openFileName = self.path + self.suffix
        return openFileName

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
        self.ws.cell(row, col).alignment = Alignment( horizontal='center', vertical='center', wrap_text=True)

        # create border per cell
        enterCell.border = Border(  top = None, left = self.thin_border, 
                                    right = self.thin_border,bottom = self.thin_border)

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
            self.ws.column_dimensions[get_column_letter(col)].width = value+3

        #Timestamps the file
        gettime = self.getTimestamp()
        Final_Report_Name = fileToSave + gettime + '.xlsx'
        self.wb.save(Final_Report_Name)
        self.suffix = "_Report_"

        return Final_Report_Name
