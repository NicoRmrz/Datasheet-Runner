from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject
import json

# User made files
from GUI_Stylesheets import GUI_Stylesheets
from parserThread import parserThread

GUI_Style = GUI_Stylesheets()

# Class: dropScript
#       Window to drag and drop input scripts
# Parameters: 
#   QListWidget - inherits QListWidget attributes
class dropScript(QListWidget):
    scriptDropped = pyqtSignal(str)
    scriptname = ""

    #initializes when class is called
    def __init__(self, parent):
        super(dropScript, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setWordWrap(True)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setStyleSheet(GUI_Style.dropWindow)

        # Instantiate parsr thread
        self.parseThread = parserThread()

        # Connect signals to slots
        self.parseThread.sendOutput.connect(self.sendOutputWindow)
        self.scriptDropped.connect(self.receiveScript)
        self.parseThread.sendDict.connect(self.getScriptDict)

# Function: receiveScript
# 		Get script path from drag and drop window
# Parameters: 
#   	script - input file path
    def receiveScript(self, script):
        self.parseThread.setScriptToParse(script, True)
        self.parseThread.start()

# Function: sendOutputWindow
# 		Output message to drag and drop window
# Parameters: 
#   	message - message to send to drag and drop window
    def sendOutputWindow(self, message):
        self.addItem(message)
        self.scrollToBottom()

# Function: getScriptDict
# 		Parse JSON file and return with dict of contents
    def getScriptDict(self):
        self.sendOutputWindow("Parsing Successful!")
        DATASHEET_DICT = self.parseThread.getDict()

        # print(DATASHEET_DICT[0]) #INDEX

        # add result to dict
        for i in DATASHEET_DICT:	
            i["Result"] = 4

        # iterate items of dict
        for distro in DATASHEET_DICT:
            print(distro)

        #save JSON
        with open('test/outdata.txt', 'w') as outfile:
            json.dump(DATASHEET_DICT, outfile)

 

# Function: dragEnterEvent
# 		Pre Defined Q List widget for drag event
# Parameters: 
#   	e - Drag Enter event
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

# Function: dragMoveEvent
# 		Pre Defined Q List widget for drag move event
# Parameters: 
#   	e - Drag Move event
    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

# Function: dropEvent
# 	    Pre Defined Q List widget for drop eve
# Parameters: 
#   	e - drop event
    def dropEvent(self, e):

        # If drag drop window has url window accepts
        if e.mimeData().hasUrls:
            e.setDropAction(Qt.CopyAction)

             # get scriptname
            for url in e.mimeData().urls():
                self.scriptname = url.toLocalFile()
                
            scriptEnding = self.scriptname.split(".")

            if scriptEnding[1] =="json":
                 # Prints/ emit file path
                self.addItem("Input Script: " + self.scriptname)
                self.scrollToBottom()
                self.scriptDropped.emit(self.scriptname)

            else:
                self.addItem("Invalid Script with extension (" + scriptEnding[1] +")")
                self.scrollToBottom()

            e.accept()
        else:
            e.ignore()