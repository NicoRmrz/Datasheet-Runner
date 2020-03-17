# -*- coding: utf-8 -*-
import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject, QSize
from PyQt5.QtWidgets import QMainWindow
import json
import sip

#imports from user made file
from GUI_Stylesheets import GUI_Stylesheets
from UI_mainWindow import Ui_MainWindow
from testPhaseWidget import testPhaseWidget
from scriptPhaseWidget import scriptPhaseWidget

GUI_Style = GUI_Stylesheets()

# Current version of application - Update for new builds
appVersion = "1.0"      # Update version

# Icon Image locations
Main_path = os.getcwd() + "/"
AppliedLogo = Main_path + "/icons/AppliedLogo.png"
nextIdle = Main_path + "/icons/nextIdle.png"
nextPressed = Main_path + "/icons/nextPressed.png"
prevIdle = Main_path + "/icons/previousIdle.png"
prevPressed = Main_path + "/icons/prevPressed.png"

os.chdir(Main_path)  #update to a local location.

NETWORK_LOC = "//energydata1/Data/Project/EA030 Generator/Prototype/Datasheet_Runner/"
SAVE_SESSION = NETWORK_LOC + 'Saved_Sessions/'
REPORT_LOC = NETWORK_LOC + 'Report/'

if not os.path.exists(SAVE_SESSION):
    os.makedirs(SAVE_SESSION)

if not os.path.exists(REPORT_LOC):
    os.makedirs(REPORT_LOC)


# Class: MainWindow
# Parameters: 
#   QMainWindow - inherits QMainWindow attributes
#   Ui_MainWindow - all objects made from UI_Mainwindow are 
# #                 brought to the MainWindow class
class MainWindow(QMainWindow, Ui_MainWindow):
    DATASHEET_DICT = {}
    current_Dict = {}
    INDEX = 0   # dictionary index
    ProtocolName = ""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Datasheet Runner v" + appVersion)
        self.setWindowIcon(QIcon(AppliedLogo))

        # Connect signals to slots
        self.scriptPhaseUI.dropWindow.parseThread.sendDict.connect(self.getScriptDict)
        self.scriptPhaseUI.dropWindow.parseThread.sendName.connect(self.getName)
        self.scriptPhaseUI.removeInstance.connect(self.testingPhase)

    # Function: updateTestGUI
    # 		Function to populate UI objects with first index of input dict
    def updateTestGUI(self):
        #Save previous data
        self.saveData()

        # set current Test outline row
        self.testPhaseUI.testOutline.setCurrentRow(self.INDEX)

        # index test
        self.current_Dict = self.DATASHEET_DICT[self.INDEX]

        # populate objects
        self.testPhaseUI.section.setText(self.current_Dict.get('Section'))     # Section
        self.testPhaseUI.test.setText(self.current_Dict.get('Test'))           # Test Name
        self.testPhaseUI.minInput.setText(self.current_Dict.get('Min'))        # Min
        self.testPhaseUI.maxInput.setText(self.current_Dict.get('Max'))        # Max
        self.testPhaseUI.unitInput.setText(self.current_Dict.get('Unit'))      # Unit
        self.testPhaseUI.comment.setText(self.current_Dict.get('Comment'))     # Comment
        self.testPhaseUI.valueInput.setText(self.current_Dict.get('Value'))    # Value
        self.testPhaseUI.passFailInput.setText(self.current_Dict.get('Result')) # Pass/ Fail 

    # -------------------------------------------------
    # --------------- SLOT Functions ------------------
    # ------------------------------------------------- 
    @pyqtSlot()
    # Function: sendStatusMessage
    # 		Slot to send a status bar message
    # Parameters: 
    #   	message -  message to show on status bar
    #   	time -  time for message to show
    def sendStatusMessage(self, message, time):
        self.statusBar.showMessage(message, time)

    # Function: testingPhase
    # 		Slot to handle removing objects on first script parsing phase 
    #       and adding UI objecs to next testing phase
    def testingPhase(self):
        # remove object from first phase
        self.FinalLayout.removeWidget(self.scriptPhaseUI)
        sip.delete(self.scriptPhaseUI)
        self.scriptPhaseUI = None

        # set up new UI for next phase
        self.testPhaseUI = testPhaseWidget(self)
        self.FinalLayout.addWidget(self.testPhaseUI)
        self.titleLayout.addLayout(self.testPhaseUI.saveResetLay)

        # Connect signals to slots
        self.testPhaseUI.resetButton.pressed.connect(self.resetPressed)
        self.testPhaseUI.resetButton.released.connect(self.resetToScriptPhase)
        self.testPhaseUI.saveButton.pressed.connect(self.savepressed)
        self.testPhaseUI.saveButton.released.connect(self.saveReleased)
        self.testPhaseUI.prevButton.pressed.connect(self.prevPressed)
        self.testPhaseUI.prevButton.released.connect(self.prevReleased)
        self.testPhaseUI.nextButton.pressed.connect(self.nextPressed)
        self.testPhaseUI.nextButton.released.connect(self.nextReleased)
        self.testPhaseUI.testOutline.itemClicked.connect(self.testClicked)

        # Update each UI entry with input dict
        self.updateTestGUI()

        # populate test outline QlistWidget
        for i in self.DATASHEET_DICT:
            self.testPhaseUI.testOutline.addItem(i.get('Section'))

    # Function: getScriptDict
    # 		Parse JSON file and return with dict of contents
    def getScriptDict(self):
        self.scriptPhaseUI.dropWindow.sendOutputWindow("Parsing Successful!")
        self.scriptPhaseUI.buttonEnable(True)

        # get dictionaty from JSON file
        self.DATASHEET_DICT = self.scriptPhaseUI.dropWindow.parseThread.getDict()

    # ------------------------------------------------------------------
    # ---------------------- Reset Session -----------------------------
    # ------------------------------------------------------------------ 
    # Function: resetPressed
    # 		Slot to handle reseting button pressed
    def resetPressed(self):
        self.testPhaseUI.resetButton.setStyleSheet(GUI_Style.buttonPressed)
        self.saveData()


    # Function: resetToScriptPhase
    # 		Slot to handle reseting to first input script phase
    def resetToScriptPhase(self):
        #reset button 
        self.testPhaseUI.resetButton.setStyleSheet(GUI_Style.resetButtonIdle)

        # reset dict index
        self.INDEX = 0

        # remove objects from second phase
        self.testPhaseUI.saveResetLay.removeWidget(self.testPhaseUI.saveButton)
        self.testPhaseUI.saveResetLay.removeWidget(self.testPhaseUI.resetButton)
        self.FinalLayout.removeWidget(self.testPhaseUI)
        sip.delete(self.testPhaseUI.saveButton)
        sip.delete(self.testPhaseUI.resetButton)
        sip.delete(self.testPhaseUI)
        self.testPhaseUI.saveButton = None
        self.testPhaseUI.resetButton = None
        self.testPhaseUI = None
   
        # Set up UI objects to first phase
        self.scriptPhaseUI = scriptPhaseWidget(self)
        self.FinalLayout.addWidget(self.scriptPhaseUI)

        # Connect signals to slots
        self.scriptPhaseUI.removeInstance.connect(self.testingPhase)
        self.scriptPhaseUI.dropWindow.parseThread.sendDict.connect(self.getScriptDict)
        self.scriptPhaseUI.dropWindow.parseThread.sendName.connect(self.getName)

    # ------------------------------------------------------------------
    # ---------------------- Save Session ------------------------------
    # ------------------------------------------------------------------  
    # Function: savepressed
    # 		Slot to handle save button pressed
    def savepressed(self):
        self.testPhaseUI.saveButton.setStyleSheet(GUI_Style.buttonPressed)

    # Function: saveReleased
    # 		Slot to handle save button released
    def saveReleased(self):
        self.testPhaseUI.saveButton.setStyleSheet(GUI_Style.buttonIdle)

        # self.saveData()

    # Function: saveData
    # 		Slot to handle save use rinput data  
    def saveData (self):
        # add input data to dict
        self.current_Dict["Value"] = self.testPhaseUI.valueInput.text()
        self.current_Dict["Result"] = self.testPhaseUI.passFailInput.text()
        self.current_Dict["Comment"] = self.testPhaseUI.comment.toPlainText()

      #save JSON
        with open(SAVE_SESSION + self.ProtocolName +'_SAVE.json', 'w') as outfile:
            json.dump(self.DATASHEET_DICT, outfile)

    # Function: getName
    # 		Slot to receive input script name to name savedsession JSON file
    # Parameters: 
    #   	inputName -  input script name to save to class variable for naming saved session file
    def getName (self, inputName):
        self.ProtocolName = inputName

    # ------------------------------------------------------------------
    # ---------------------- Previous Test -----------------------------
    # ------------------------------------------------------------------ 
    # Function: prevPressed
    # 		Slot to handle previous button pressed
    def prevPressed(self):
        self.testPhaseUI.prevButton.setIcon(QIcon(prevPressed))

    # Function: prevReleased
    # 		Slot to handle previous button released
    def prevReleased(self):
        self.testPhaseUI.prevButton.setIcon(QIcon(prevIdle))
        if (self.INDEX != 0):
            self.INDEX = self.INDEX - 1
        else:
            self.sendStatusMessage("Reached the beginning of the tests", 1000)

        # Update each UI entry with input dict
        self.updateTestGUI()
    # ------------------------------------------------------------------
    # ---------------------- Next Test ---------------------------------
    # ------------------------------------------------------------------ 
    # Function: nextPressed
    # 		Slot to handle next button pressed
    def nextPressed(self):
        self.testPhaseUI.nextButton.setIcon(QIcon(nextPressed))

    # Function: nextReleased
    # 		Slot to handle next button released
    def nextReleased(self):
        self.testPhaseUI.nextButton.setIcon(QIcon(nextIdle))
        if (self.INDEX < len(self.DATASHEET_DICT)-1):
            self.INDEX = self.INDEX + 1
        else:
            self.sendStatusMessage("Reached the end of the tests", 1000)

        # Update each UI entry with input dict
        self.updateTestGUI()

    # ------------------------------------------------------------------
    # ------------------  Test Outline Clicked -------------------------
    # ------------------------------------------------------------------ 
    # Function: testClicked
    # 		Slot to handle item click in QListWidget
    def testClicked(self, item):
        self.INDEX = self.testPhaseUI.testOutline.row(item)

        # Update each UI entry with input dict
        self.updateTestGUI()

    # ------------------------------------------------------------------
    # ----------- Close All Threads at app closure ---------------------
    # ------------------------------------------------------------------             
    # Stop all threads when GUI is closed
    def closeEvent(self, *args, **kwargs):
        if(self.scriptPhaseUI != None):
            self.scriptPhaseUI.dropWindow.parseThread.terminate
            self.scriptPhaseUI.dropWindow.parseThread.wait(100)  
        else:
            self.saveData()
      
        sys.exit(0)