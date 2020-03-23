# -*- coding: utf-8 -*-
import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap, QIcon, QColor,QBrush
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject, QSize, QRegularExpression, QFile
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
import json
import sip
from enum import Enum

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

# Saved session and exel report locations
# NETWORK_LOC = "//energydata1/Data/Project/EA030 Generator/Prototype/Datasheet_Runner/"
NETWORK_LOC = Main_path + "test/"
SAVE_SESSION = NETWORK_LOC + 'Saved_Sessions/'
REPORT_LOC = NETWORK_LOC + 'Report/'

if not os.path.exists(SAVE_SESSION):
    os.makedirs(SAVE_SESSION)

if not os.path.exists(REPORT_LOC):
    os.makedirs(REPORT_LOC)

'''
Function: enum
    To support automatic enumeration

Returns:
    Enumeration 
'''
def enum(**enums):
    return type('Enum', (), enums)

'''
Enum: EQUIPMENT_TYPE 
    Enumeration created to define the Equipment Section Names of the JSON file

    equipment   - equipment dictionary section of JSON file
    tools       - tools dictionary section of JSON file
    material    - material dictionary section of JSON file
'''
EQUIPMENT_TYPE = enum(equipment = "Equipment", tools = "Tools", material = "Material")

'''
Enum: TEST_TYPE
    Enumeration created to define the test types for the procedure sections.
    More can be defined here later on.

    numeric   - numeric test type to test value against min and max
    bool      - boolean test type only accepts pass or fail
'''
TEST_TYPE = enum(numeric = "numeric", bool = "bool")

'''
Class: MainWindow

Parameters: 
    QMainWindow - inherits QMainWindow attributes
    Ui_MainWindow - all objects made from UI_Mainwindow are 
                    brought to the MainWindow class
'''
class MainWindow(QMainWindow, Ui_MainWindow):
    DATASHEET_DICT = {}
    current_Dict = {}
    INDEX = 0   # dictionary index
    serNum = ""
    EQUIP_INDEX = 0 # equipment list index
    SPEC_INDEX = 0 # Specific index for writing the quipment to their repective JSON categories. Index is indexed with EQUIP_INDEX
    PREV_EQUIP_INDEX = 0
    PREV_SPEC_INDEX = 0
    EquipmentList =[]   # list to hold all the dictionaries of all sections of equipment
    IterJSONList = []   # list to show specific index of each equipment item in their respective section in the JSON file

    '''
    Function: __init__
		initializes when class is called
    '''
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Datasheet Runner v" + appVersion)
        self.setWindowIcon(QIcon(AppliedLogo))

        # Connect signals to slots
        self.scriptPhaseUI.dropWindow.parseThread.sendDict.connect(self.getScriptDict)
        self.scriptPhaseUI.removeInstance.connect(self.testingPhase)
        self.serNumInput.textChanged.connect(self.checkSerialNumber)

    # -------------------------------------------------
    # --------------- Populate GUI --------------------
    # ------------------------------------------------- 
    '''
    Function: updateTestGUI
        Function to populate UI objects with first index of input dict
    '''
    def updateTestGUI(self):
        #Save previous data
        self.saveData()
     
        # set current Test outline row
        self.testPhaseUI.testOutline.setCurrentRow(self.INDEX)

        # index test
        self.current_Dict = self.DATASHEET_DICT["Procedure"][self.INDEX]

        # populate objects
        self.testPhaseUI.section.setText(self.current_Dict.get('Section'))     # Section
        self.testPhaseUI.test.setText(self.current_Dict.get('Test'))           # Test Name

        # populate empty Min fields wit N/A
        if (self.current_Dict.get('Min')== ''):
            self.testPhaseUI.minInput.setText("N/A")
            self.current_Dict["Min"] = self.testPhaseUI.minInput.text()
        else:
            self.testPhaseUI.minInput.setText(self.current_Dict.get('Min'))        
        
        # populate empty Max fields wit N/A
        if (self.current_Dict.get('Max')== ''):
            self.testPhaseUI.maxInput.setText("N/A")
            self.current_Dict["Max"] = self.testPhaseUI.maxInput.text()
        else:
            self.testPhaseUI.maxInput.setText(self.current_Dict.get('Max'))        

        # populate empty Unit fields wit N/A
        if (self.current_Dict.get('Unit')== ''):
            self.testPhaseUI.unitInput.setText("N/A")
            self.current_Dict["Unit"] = self.testPhaseUI.unitInput.text()
        else:
            self.testPhaseUI.unitInput.setText(self.current_Dict.get('Unit'))      

        self.testPhaseUI.comment.setText(self.current_Dict.get('Comment'))      # Comment
        self.testPhaseUI.valueInput.setText(self.current_Dict.get('Value'))     # Value
        self.testPhaseUI.passFailInput.setText(self.current_Dict.get('Result')) # Pass/ Fail 

        # update user input field pending test type
        if (self.current_Dict.get('Type') == TEST_TYPE.numeric):
            self.testPhaseUI.valueInput.setReadOnly(False)
            self.testPhaseUI.valueInput.setStyleSheet(GUI_Style.inputBox)
            self.testPhaseUI.passFailInput.setReadOnly(True)
            self.testPhaseUI.passFailInput.setStyleSheet(GUI_Style.passFail)

        elif (self.current_Dict.get('Type') == TEST_TYPE.bool):
            self.testPhaseUI.valueInput.setReadOnly(True)
            self.testPhaseUI.valueInput.setStyleSheet(GUI_Style.inputBoxNonEdit)
            self.testPhaseUI.passFailInput.setReadOnly(False)
            self.testPhaseUI.passFailInput.setStyleSheet(GUI_Style.passFailInput)
        
        # color tests if populated
        if (self.testPhaseUI.passFailInput.text() == "P"):
            self.setPassFail("Pass")
        elif (self.testPhaseUI.passFailInput.text() == "F"):
            self.setPassFail("Fail")

    '''
    Function: setPassFail
        Color fields and set pass or fail

    Parameters:
        state - pass or fail state
    '''
    def setPassFail(self, state):
        # get current Qlistwidget item from list
        item = QListWidgetItem(self.testPhaseUI.testOutline.takeItem(self.INDEX))

        # color P/F field and listwidget
        if (state == "Pass"):
            self.testPhaseUI.passFailInput.setText("P")
            self.testPhaseUI.passFailInput.setStyleSheet(GUI_Style.passedTest)           
            item.setBackground(QColor("green"))

        elif (state == "Fail"):
            self.testPhaseUI.passFailInput.setText("F")
            self.testPhaseUI.passFailInput.setStyleSheet(GUI_Style.failedTest)
            item.setBackground(QColor("red"))

        else:
            # Set P/F stylesheet pending type of test
            if (self.current_Dict.get('Type') == TEST_TYPE.numeric):
                self.testPhaseUI.passFailInput.setStyleSheet(GUI_Style.passFail)
            else:
                self.testPhaseUI.passFailInput.setStyleSheet(GUI_Style.passFailInput)

            item.setBackground(QColor("#20292F"))   #backgorund color

        self.testPhaseUI.testOutline.insertItem(self.INDEX, item)
        self.testPhaseUI.testOutline.setCurrentItem(item)

        # if length of input JSON dictionary is less than QListWidget rows then remove last item.
        # issue found when restoring a saved session a extra row was added.
        if (len(self.DATASHEET_DICT["Procedure"]) < self.testPhaseUI.testOutline.count()):
            self.testPhaseUI.testOutline.takeItem(self.testPhaseUI.testOutline.count()-1)

    # -------------------------------------------------
    # --------------- SLOT Functions ------------------
    # ------------------------------------------------- 
    '''
    Function: sendStatusMessage
        Slot to send a status bar message

    Parameters: 
      	message -  message to show on status bar
      	time -  time for message to show
    '''
    @pyqtSlot()
    def sendStatusMessage(self, message, time):
        self.statusBar.showMessage(message, time)

    '''
    Function: testingPhase
        Slot to handle removing objects on first script parsing phase 
        and adding UI objecs to next testing phase
    '''
    def testingPhase(self):
        # save and lock serial number
        self.serNum = self.serNumInput.text()
        self.serNumInput.setReadOnly(True)
        self.serNumInput.setText("S/N: " + self.serNum)
        self.DATASHEET_DICT['Serial Number'] = self.serNum
        
        # remove object from first phase
        self.FinalLayout.removeWidget(self.scriptPhaseUI)
        sip.delete(self.scriptPhaseUI)
        self.scriptPhaseUI = None

        # set up new UI for next phase
        self.testPhaseUI = testPhaseWidget(self)
        self.FinalLayout.addWidget(self.testPhaseUI)
        self.statusBar.addPermanentWidget(self.testPhaseUI.equipmentButton, 0)
        self.statusBar.addPermanentWidget(self.testPhaseUI.resetButton, 0)
        self.statusBar.addPermanentWidget(self.testPhaseUI.submitButton, 0)

        # Connect signals to slots
        self.testPhaseUI.resetButton.pressed.connect(self.resetPressed)
        self.testPhaseUI.resetButton.released.connect(self.resetToScriptPhase)
        self.testPhaseUI.submitButton.pressed.connect(self.submitPressed)
        self.testPhaseUI.submitButton.released.connect(self.submitReleased)
        self.testPhaseUI.equipmentButton.pressed.connect(self.euipmentPressed)
        self.testPhaseUI.equipmentButton.released.connect(self.equipmentReleased)
        self.testPhaseUI.prevButton.pressed.connect(self.prevPressed)
        self.testPhaseUI.prevButton.released.connect(self.prevReleased)
        self.testPhaseUI.nextButton.pressed.connect(self.nextPressed)
        self.testPhaseUI.nextButton.released.connect(self.nextReleased)
        self.testPhaseUI.valueInput.textChanged.connect(self.numericAcceptanceCriteria)
        self.testPhaseUI.passFailInput.textChanged.connect(self.booleanAcceptanceCriteria)
        self.testPhaseUI.testOutline.itemClicked.connect(self.testClicked)
        self.testPhaseUI.equipPopup.equipmentListWidget.itemClicked.connect(self.equipmentClicked)
        self.testPhaseUI.equipPopup.finished.connect(self.equipFinished)
        self.testPhaseUI.excelReportThread.sendReportName.connect(self.reportDone)

        # Update each UI entry with input dict
        self.testPhaseUI.testOutline.clear()
        self.updateTestGUI()

        # populate test outline QlistWidget
        for i in self.DATASHEET_DICT["Procedure"]:
            item = QListWidgetItem(i.get('Section'))

            # color list item if result is populated
            if (i.get('Result') == 'P'):
                item.setBackground(QColor("green"))
            elif (i.get('Result') == 'F'):
                item.setBackground(QColor("red"))

            self.testPhaseUI.testOutline.insertItem(self.INDEX, item)
            self.INDEX = self.INDEX + 1 # incremement index

        # if length of input JSON dictionary is less than QListWidget rows then remove last item.
        # issue found when restoring a saved session a extra row was added.
        if (len(self.DATASHEET_DICT["Procedure"]) < self.testPhaseUI.testOutline.count()):
            self.testPhaseUI.testOutline.takeItem(self.testPhaseUI.testOutline.count()-1)

        # select first item
        self.INDEX = 0
        self.testPhaseUI.testOutline.setCurrentRow(self.INDEX)

        self.populateEquipmentList()

    '''
    Function: getScriptDict
        Parse JSON file and return with dict of contents. 
        Perform final checks for valid script
    '''
    def getScriptDict(self):
        success = True

        # get dictionary from JSON file
        self.DATASHEET_DICT = self.scriptPhaseUI.dropWindow.parseThread.getDict()
        
        # first check for procedure in dict
        if  ("Procedure" not in self.DATASHEET_DICT):
            self.scriptPhaseUI.dropWindow.sendOutputWindow("Invalid JSON file. Missing Test Procedure")
            success = False

        else:
            # populate serial number if set 
            if (self.DATASHEET_DICT.get('Serial Number') == ""):
                self.serNumInput.setText("")
                self.serNumInput.setPlaceholderText("Enter Serial Number")
            else:
                self.serNumInput.setText(self.DATASHEET_DICT.get('Serial Number'))

            # Check for valid test type
            for i in self.DATASHEET_DICT["Procedure"]:    
                if ((i.get('Type') != TEST_TYPE.numeric) and (i.get('Type') != TEST_TYPE.bool)):  
                    self.scriptPhaseUI.dropWindow.sendOutputWindow("Invalid Test Type '" + i.get('Type') + "' in JSON file")
                    success = False

        # successfull 
        if (success):
            self.scriptPhaseUI.dropWindow.sendOutputWindow("Parsing Successful!")

            # check if serial number is populated and valid
            self.checkSerialNumber() 

        else:
            self.scriptPhaseUI.dropWindow.sendOutputWindow("Parsing Failed!")
            self.scriptPhaseUI.buttonEnable(False)                

    '''
    Function: checkSerialNumber
        Ensure a Serial Number has been entered. Check character that no special characters are in name
    '''
    def checkSerialNumber(self):
        specialChar =  QRegularExpression("[@!#$%^&*()<>?/\|}{~:]") 
        specialMatch = specialChar.match(self.serNumInput.text()).hasMatch() # check for special character
        res = not self.DATASHEET_DICT   # check for empty dic

        # Must be in first phase and have a JSON dictionary
        if(self.scriptPhaseUI != None and res == False):
            if (self.serNumInput.text() != "" and specialMatch == False):
                self.scriptPhaseUI.buttonEnable(True)
            else:
                # ensure no special characters are used
                if (specialMatch):
                    # Only check special characters in first phase
                    if (self.serNumInput.isReadOnly() == False): 
                        self.sendStatusMessage("Invalid Special Character", 1000)
                else:
                    self.sendStatusMessage("Enter Serial Number", 1000)
                self.scriptPhaseUI.buttonEnable(False) 
        else:
            self.sendStatusMessage("Drag New JSON File", 2000)

    # ------------------------------------------------------------------
    # ------------------ Acceptance Criteria ---------------------------
    # ------------------------------------------------------------------ 
    '''
    Function: numericAcceptanceCriteria
    		Slot to perform the numeric acceptance criteria.

    Parameters:
          inputText - every input calculates current acceptance criteria
    '''
    def numericAcceptanceCriteria(self, inputText):
        if((inputText != '') and (inputText.isspace()==False) and (self.testPhaseUI.valueInput.isReadOnly() == False)):
            run = True
            testVal = 0
            minAC = 0
            maxAC = 0

            #  set reguar expression value to 
            isHex = QRegularExpression("0x+[0-9a-f]", QRegularExpression.CaseInsensitiveOption) # hex number
            dontConvert = QRegularExpression("x+", QRegularExpression.CaseInsensitiveOption)    # dont convert 0x or just x
            isAlphabet = QRegularExpression("[a-z]", QRegularExpression.CaseInsensitiveOption)   # look for alphabet characters
            isNonHexAlphabet = QRegularExpression("[g-z]", QRegularExpression.CaseInsensitiveOption)   # look for alphabet characters non hex
        
            # check base and convert to int
            if (isHex.match(inputText).hasMatch()):
                testVal = int(inputText, 16)    # convert hex val to int

            elif ((dontConvert.match(inputText).hasMatch() == False) and (isAlphabet.match(inputText).hasMatch() == False)):
                testVal = inputText

            elif (isNonHexAlphabet.match(inputText).hasMatch()):
                run = False

            if (run):
                testVal = float(testVal)
                if (self.testPhaseUI.minInput.text() !=''):
                    minAC =  float(self.testPhaseUI.minInput.text())
                if (self.testPhaseUI.maxInput.text() !=''):
                    maxAC =  float(self.testPhaseUI.maxInput.text())

                if (testVal < minAC or testVal > maxAC):
                    self.setPassFail("Fail")
                else:
                    self.setPassFail("Pass")

            else:
                self.sendStatusMessage("Invalid Input", 1000)
                self.setPassFail("Fail")

        # clear if empty
        else:
            self.testPhaseUI.passFailInput.setText("")
            self.setPassFail("Reset")

    '''
    Function: booleanAcceptanceCriteria
    		Slot to perform acceptance criteria on boolean tests

    Parameters:
          inputText - input pass or fail
    '''
    def booleanAcceptanceCriteria(self, inputText):
        if(self.testPhaseUI.passFailInput.isReadOnly() == False):
            if(inputText != ''):
                isPass = QRegularExpression("p", QRegularExpression.CaseInsensitiveOption)
                isFail = QRegularExpression("f", QRegularExpression.CaseInsensitiveOption)

                if (isPass.match(inputText).hasMatch()):
                    self.setPassFail("Pass")
                elif (isFail.match(inputText).hasMatch()):
                    self.setPassFail("Fail")
                else:
                    self.setPassFail("Fail")
                    self.sendStatusMessage("Invalid Input", 1000)
                    self.testPhaseUI.passFailInput.setStyleSheet(GUI_Style.passFailInput)
        
            # clear if empty
            else:
                self.setPassFail("Reset")            

    # ------------------------------------------------------------------
    # ---------------------- Reset Session -----------------------------
    # ------------------------------------------------------------------ 
    '''
    Function: resetPressed
    		Slot to handle reseting button pressed
    '''
    def resetPressed(self):
        self.testPhaseUI.resetButton.setStyleSheet(GUI_Style.statusButtonPressed)

    '''
    Function: resetToScriptPhase
    		Slot to handle reseting to first input script phase
    '''
    def resetToScriptPhase(self):
        self.serNumInput.setReadOnly(False)
        self.serNumInput.setText(" ")

        #reset button 
        self.testPhaseUI.resetButton.setStyleSheet(GUI_Style.resetButtonIdle)

        #save last data
        self.saveData()

        # clear dict for next run
        self.DATASHEET_DICT.clear()

        # reset dict and equip list index
        self.INDEX = 0
        self.EQUIP_INDEX = 0
        self.SPEC_INDEX = 0

        # remove objects from second phase
        self.statusBar.removeWidget(self.testPhaseUI.submitButton)
        self.statusBar.removeWidget(self.testPhaseUI.resetButton)
        self.statusBar.removeWidget(self.testPhaseUI.equipmentButton)
        self.FinalLayout.removeWidget(self.testPhaseUI)
        sip.delete(self.testPhaseUI.submitButton)
        sip.delete(self.testPhaseUI.resetButton)
        sip.delete(self.testPhaseUI.equipmentButton)
        sip.delete(self.testPhaseUI)
        self.testPhaseUI.submitButton = None
        self.testPhaseUI.resetButton = None
        self.testPhaseUI.equipmentButton = None
        self.testPhaseUI = None
   
        # Set up UI objects to first phase
        self.scriptPhaseUI = scriptPhaseWidget(self)
        self.FinalLayout.addWidget(self.scriptPhaseUI)

        # Connect signals to slots
        self.scriptPhaseUI.removeInstance.connect(self.testingPhase)
        self.scriptPhaseUI.dropWindow.parseThread.sendDict.connect(self.getScriptDict)

    # ------------------------------------------------------------------
    # --------------------  Generate Report ----------------------------
    # ------------------------------------------------------------------  
    '''
    Function: submitPressed
        Slot to handle submit button pressed
    '''
    def submitPressed(self):
        self.testPhaseUI.submitButton.setStyleSheet(GUI_Style.statusButtonPressed)

    '''
    Function: submitReleased
        Slot to handle submit button released
    '''
    def submitReleased(self):
        self.testPhaseUI.submitButton.setStyleSheet(GUI_Style.statusButtonIdle)

        #save last data
        self.saveData()

        # generate report and disable button until procedure has finished
        self.testPhaseUI.excelReportThread.setGenerateExcel(self.DATASHEET_DICT, REPORT_LOC, "testNAME", True)
        self.testPhaseUI.excelReportThread.start()
        self.testPhaseUI.submitButton.setEnabled(False)

    '''
    Function: reportDone
        Slot to receive report name when excell sheet has finished being populated

    Parameters:
        name - excel report name  
    '''
    def reportDone(self, name):
        self.sendStatusMessage("Report: " + name, 20000)
        self.testPhaseUI.submitButton.setEnabled(True)

        # Remove saved session once complete
        fileToRemove = QFile(SAVE_SESSION + 'outData.json')
        if (fileToRemove.exists()):
            fileToRemove.remove()
 
    '''
    Function: saveData
        Slot to handle save use rinput data  
    '''
    def saveData (self):
        # add input data to dict
        self.current_Dict["Value"] = self.testPhaseUI.valueInput.text()
        self.current_Dict["Result"] = self.testPhaseUI.passFailInput.text()
        self.current_Dict["Comment"] = self.testPhaseUI.comment.toPlainText()

      #save JSON
        with open(SAVE_SESSION + 'outData.json', 'w') as outfile:
            json.dump(self.DATASHEET_DICT, outfile)

    # ------------------------------------------------------------------
    # --------------------  Add Equipment ------------------------------
    # ------------------------------------------------------------------  
    '''
    Function: euipmentPressed
        Slot to handle equipment button pressed
    '''
    def euipmentPressed(self):
        self.testPhaseUI.equipmentButton.setStyleSheet(GUI_Style.statusButtonPressed)

    '''
    Function: equipmentReleased
        Slot to handle equipment button released
    '''
    def equipmentReleased(self):
        self.testPhaseUI.equipmentButton.setStyleSheet(GUI_Style.statusEquipButtonIdle)
        self.testPhaseUI.equipPopup.exec_()

    '''
    Function: populateEquipmentList
        Function to populate QlistWdiget of equipment from dicitonary when entering testing Phase
    '''
    def populateEquipmentList(self):
        self.testPhaseUI.equipPopup.equipmentListWidget.clear()
        self.IterJSONList.clear()
        self.EquipmentList.clear()
        equiCnt = 0 # authenic iterator index per section
        toolCnt = 0
        matCnt = 0

        # Add equipment 
        for i in self.DATASHEET_DICT[EQUIPMENT_TYPE.equipment]:
            # only add items with names
            if (i.get('Name') != ""):
                equip_item = QListWidgetItem(i.get('Name'))
                equip_item.setData(Qt.UserRole, EQUIPMENT_TYPE.equipment) # set equip type
                self.testPhaseUI.equipPopup.equipmentListWidget.insertItem(self.EQUIP_INDEX, equip_item)
                self.EquipmentList.append(i)    # add equip to list
                self.IterJSONList.append(equiCnt)    # add to JSON iterator list for writing
                self.EQUIP_INDEX = self.EQUIP_INDEX + 1 # incremement index
                equiCnt +=1

        # Add tools
        for i in self.DATASHEET_DICT[EQUIPMENT_TYPE.tools]:
             # only add items with names
            if (i.get('Name') != ""):
                equip_item = QListWidgetItem(i.get('Name'))
                equip_item.setData(Qt.UserRole, EQUIPMENT_TYPE.tools) # set equip type
                self.testPhaseUI.equipPopup.equipmentListWidget.insertItem(self.EQUIP_INDEX, equip_item)
                self.EquipmentList.append(i)    # add equip to list
                self.IterJSONList.append(toolCnt)    # add to JSON iterator list for writing
                self.EQUIP_INDEX = self.EQUIP_INDEX + 1 # incremement index
                toolCnt +=1

        # Add materials
        for i in self.DATASHEET_DICT[EQUIPMENT_TYPE.material]:
             # only add items with names
            if (i.get('Name') != ""):
                equip_item = QListWidgetItem(i.get('Name'))
                equip_item.setData(Qt.UserRole, EQUIPMENT_TYPE.material) # set equip type
                self.testPhaseUI.equipPopup.equipmentListWidget.insertItem(self.EQUIP_INDEX, equip_item)
                self.EquipmentList.append(i)    # add equip to list
                self.IterJSONList.append(matCnt)    # add to JSON iterator list for writing
                self.EQUIP_INDEX = self.EQUIP_INDEX + 1 # incremement index
                matCnt +=1

        # select first item and setup UI
        self.EQUIP_INDEX = 0
        item = self.testPhaseUI.equipPopup.equipmentListWidget.item(self.EQUIP_INDEX)
        self.testPhaseUI.equipPopup.equipmentListWidget.setCurrentItem(item)
        self.updateEquipmentUI(item.data(Qt.UserRole))  # set UI for first item

    '''
    Function: equipmentClicked
    	Slot to handle item click in Equipment QListWidget

    Parameters:
        item - QListWidgetItem that was clicked
    '''
    def equipmentClicked(self, item):
        self.EQUIP_INDEX = self.testPhaseUI.equipPopup.equipmentListWidget.row(item)

        # Update each UI entry with equipment dict and pass in equip type
        self.updateEquipmentUI(item.data(Qt.UserRole))

    '''
    Function: updateEquipmentUI
        Function to update Equipment wndow UI

    Parameters:
        equipType - type of equipment to be displayed enum [Equipment, Tools, Material]
    '''
    def updateEquipmentUI(self, equipType):

        # save equipment
        self.saveEquipment()

        # get specific item index in each category
        self.SPEC_INDEX = self.IterJSONList[self.EQUIP_INDEX]

        # update UI objects and layout
        self.testPhaseUI.equipPopup.switchEquipmentUI(equipType)

        if (equipType == EQUIPMENT_TYPE.equipment):
            self.testPhaseUI.equipPopup.equipmentWidget.modelInput.setText(self.DATASHEET_DICT[EQUIPMENT_TYPE.equipment][self.SPEC_INDEX].get('Model'))
            self.testPhaseUI.equipPopup.equipmentWidget.equipmentIDInput.setText(self.DATASHEET_DICT[EQUIPMENT_TYPE.equipment][self.SPEC_INDEX].get('ID'))
            self.testPhaseUI.equipPopup.equipmentWidget.calibrationIDInput.setText(self.DATASHEET_DICT[EQUIPMENT_TYPE.equipment][self.SPEC_INDEX].get('Cal ID'))
            self.testPhaseUI.equipPopup.equipmentWidget.calDueDateInput.setText(self.DATASHEET_DICT[EQUIPMENT_TYPE.equipment][self.SPEC_INDEX].get('Cal Due Date'))   
 
        elif (equipType == EQUIPMENT_TYPE.tools):
            self.testPhaseUI.equipPopup.toolWidget.versionInput.setText(self.DATASHEET_DICT[EQUIPMENT_TYPE.tools][self.SPEC_INDEX].get('Version'))

        elif (equipType == EQUIPMENT_TYPE.material):
            self.testPhaseUI.equipPopup.materialWidget.serialInput.setText(self.DATASHEET_DICT[EQUIPMENT_TYPE.material][self.SPEC_INDEX].get('Serial Number'))
            self.testPhaseUI.equipPopup.materialWidget.revisionInput.setText(self.DATASHEET_DICT[EQUIPMENT_TYPE.material][self.SPEC_INDEX].get('Revision'))
            self.testPhaseUI.equipPopup.materialWidget.firmwareInput.setText(self.DATASHEET_DICT[EQUIPMENT_TYPE.material][self.SPEC_INDEX].get('Firmware'))
            self.testPhaseUI.equipPopup.materialWidget.softwareInput.setText(self.DATASHEET_DICT[EQUIPMENT_TYPE.material][self.SPEC_INDEX].get('Software'))

        # set previos indexs
        self.PREV_SPEC_INDEX  =  self.SPEC_INDEX
        self.PREV_EQUIP_INDEX =  self.EQUIP_INDEX

    '''
    Function: saveEquipment
        Function to save equipment to a local equipment list and to the JSON session file
    '''
    def saveEquipment(self):
        item = self.testPhaseUI.equipPopup.equipmentListWidget.item(self.PREV_EQUIP_INDEX)

        if (item.data(Qt.UserRole) == EQUIPMENT_TYPE.equipment and self.testPhaseUI.equipPopup.equipmentWidget != None):
            self.EquipmentList[self.PREV_EQUIP_INDEX]["Model"] = self.testPhaseUI.equipPopup.equipmentWidget.modelInput.text()      # Save Model
            self.EquipmentList[self.PREV_EQUIP_INDEX]["ID"] = self.testPhaseUI.equipPopup.equipmentWidget.equipmentIDInput.text()   # Equpment ID
            self.EquipmentList[self.PREV_EQUIP_INDEX]["Cal ID"] = self.testPhaseUI.equipPopup.equipmentWidget.calibrationIDInput.text()   # Calibration ID
            self.EquipmentList[self.PREV_EQUIP_INDEX]["Cal Due Date"] = self.testPhaseUI.equipPopup.equipmentWidget.calDueDateInput.text()   # Calibration Due Date

            self.DATASHEET_DICT[EQUIPMENT_TYPE.equipment][self.PREV_SPEC_INDEX]["Model"] =  self.EquipmentList[self.PREV_EQUIP_INDEX]["Model"]
            self.DATASHEET_DICT[EQUIPMENT_TYPE.equipment][self.PREV_SPEC_INDEX]["ID"] =  self.EquipmentList[self.PREV_EQUIP_INDEX]["ID"]
            self.DATASHEET_DICT[EQUIPMENT_TYPE.equipment][self.PREV_SPEC_INDEX]["Cal ID"] =  self.EquipmentList[self.PREV_EQUIP_INDEX]["Cal ID"]
            self.DATASHEET_DICT[EQUIPMENT_TYPE.equipment][self.PREV_SPEC_INDEX]["Cal Due Date"] =  self.EquipmentList[self.PREV_EQUIP_INDEX]["Cal Due Date"]

        elif (item.data(Qt.UserRole) == EQUIPMENT_TYPE.tools):
            self.EquipmentList[self.PREV_EQUIP_INDEX]["Version"] = self.testPhaseUI.equipPopup.toolWidget.versionInput.text()      # Save Version

            self.DATASHEET_DICT[EQUIPMENT_TYPE.tools][self.PREV_SPEC_INDEX]["Version"] =  self.EquipmentList[self.PREV_EQUIP_INDEX]["Version"]

        elif (item.data(Qt.UserRole) == EQUIPMENT_TYPE.material):
            self.EquipmentList[self.PREV_EQUIP_INDEX]["Serial Number"] = self.testPhaseUI.equipPopup.materialWidget.serialInput.text()      # Save Serial Number
            self.EquipmentList[self.PREV_EQUIP_INDEX]["Revision"] = self.testPhaseUI.equipPopup.materialWidget.revisionInput.text()      # Save Revision
            self.EquipmentList[self.PREV_EQUIP_INDEX]["Firmware"] = self.testPhaseUI.equipPopup.materialWidget.firmwareInput.text()      # Save Firmware
            self.EquipmentList[self.PREV_EQUIP_INDEX]["Software"] = self.testPhaseUI.equipPopup.materialWidget.softwareInput.text()      # Save Software

            self.DATASHEET_DICT[EQUIPMENT_TYPE.material][self.PREV_SPEC_INDEX]["Serial Number"] =  self.EquipmentList[self.PREV_EQUIP_INDEX]["Serial Number"]
            self.DATASHEET_DICT[EQUIPMENT_TYPE.material][self.PREV_SPEC_INDEX]["Revision"] =  self.EquipmentList[self.PREV_EQUIP_INDEX]["Revision"]
            self.DATASHEET_DICT[EQUIPMENT_TYPE.material][self.PREV_SPEC_INDEX]["Firmware"] =  self.EquipmentList[self.PREV_EQUIP_INDEX]["Firmware"]
            self.DATASHEET_DICT[EQUIPMENT_TYPE.material][self.PREV_SPEC_INDEX]["Software"] =  self.EquipmentList[self.PREV_EQUIP_INDEX]["Software"]
       
        #save JSON
        with open(SAVE_SESSION + 'outData.json', 'w') as outfile:
            json.dump(self.DATASHEET_DICT, outfile)    

        self.sendStatusMessage("Equipment Saved!", 1000)

    '''
    Function: equipFinished
        QDialog signal emitted when closing dialog window. Function will save equipment data

    Parameters:
        res - result emitted from closing QDialog object. Not used
    '''
    def equipFinished(self, res):
        self.saveEquipment ()

    # ------------------------------------------------------------------
    # ---------------------- Previous Test -----------------------------
    # ------------------------------------------------------------------ 
    '''
    Function: prevPressed
        Slot to handle previous button pressed
    '''
    def prevPressed(self):
        self.testPhaseUI.prevButton.setIcon(QIcon(prevPressed))

    '''
    Function: prevReleased
        Slot to handle previous button released
    '''
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
    '''
    Function: nextPressed
        Slot to handle next button pressed
    '''
    def nextPressed(self):
        self.testPhaseUI.nextButton.setIcon(QIcon(nextPressed))

    '''
    Function: nextReleased
    	Slot to handle next button released
    '''
    def nextReleased(self):
        self.testPhaseUI.nextButton.setIcon(QIcon(nextIdle))
        if (self.INDEX < len(self.DATASHEET_DICT["Procedure"])-1):
            self.INDEX = self.INDEX + 1
        else:
            self.sendStatusMessage("Reached the end of the tests", 1000)

        # Update each UI entry with input dict
        self.updateTestGUI()

    # ------------------------------------------------------------------
    # ------------------  Test Outline Clicked -------------------------
    # ------------------------------------------------------------------ 
    '''
    Function: testClicked
    	Slot to handle item click in QListWidget

    Parameters:
        item - QListWidgetItem that was clicked
    '''
    def testClicked(self, item):
        self.INDEX = self.testPhaseUI.testOutline.row(item)

        # Update each UI entry with input dict
        self.updateTestGUI()

    # ------------------------------------------------------------------
    # ----------- Close All Threads at app closure ---------------------
    # ------------------------------------------------------------------   
    '''
    Function: closeEvent
        Stop all threads when GUI is closed
    '''          
    def closeEvent(self, *args, **kwargs):
        if(self.scriptPhaseUI != None):
            self.scriptPhaseUI.dropWindow.parseThread.terminate
            self.scriptPhaseUI.dropWindow.parseThread.wait(100)  
        else:
            self.saveData()
            self.testPhaseUI.excelReportThread.terminate      
            self.testPhaseUI.excelReportThread.wait(100)       
        sys.exit(0)
