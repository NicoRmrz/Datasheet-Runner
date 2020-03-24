import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QTextEdit, QAbstractItemView,  QListWidget, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject, QSize
from PyQt5.QtGui import QPixmap, QIcon

# User made files
from GUI_Stylesheets import GUI_Stylesheets
from equipmentPopUpWidget import equipmentPopUpWidget

GUI_Style = GUI_Stylesheets()

# Icon Image locations
Main_path = os.getcwd() + "/"
nextIdle = Main_path + "/icons/nextIdle.png"
prevIdle = Main_path + "/icons/previousIdle.png"

'''
Class: testPhaseWidget
    Create widget and layout for testing phase
    
Parameters: 
    QWidget - inherits QWidget attributes
'''
class testPhaseWidget(QWidget):

    '''
    Function: __init__
		initializes when class is called
    '''
    def __init__(self, parent, excelThread):
        super(testPhaseWidget, self).__init__(parent)

        # get excel thread
        self.excelReportThread = excelThread

        # Instance pop up window
        self.equipPopup = equipmentPopUpWidget(self)

        # ----------------------------------
        # ------- Create Objects -----------
        # ----------------------------------
        # create reset phase button
        self.resetButton = QPushButton(self)
        self.resetButton.setText("Reset")
        self.resetButton.setMaximumSize(70, 25)
        self.resetButton.setMinimumSize(70, 25)
        self.resetButton.setStyleSheet(GUI_Style.resetButtonIdle)

        # create submit button
        self.submitButton = QPushButton(self)
        self.submitButton.setText("Submit")
        self.submitButton.setMaximumSize(70, 25)
        self.submitButton.setMinimumSize(70, 25)
        self.submitButton.setStyleSheet(GUI_Style.statusButtonIdle)

        # create Equipment button
        self.equipmentButton = QPushButton(self)
        self.equipmentButton.setText("Equipment")
        self.equipmentButton.setMaximumSize(100, 25)
        self.equipmentButton.setMinimumSize(100, 25)
        self.equipmentButton.setStyleSheet(GUI_Style.statusEquipButtonIdle)

        # create previous test button
        self.prevButton = QPushButton(self)
        self.prevButton.setText("")
        self.prevButton.setMaximumSize(100, 75)
        self.prevButton.setMinimumSize(100, 75)
        self.prevButton.setStyleSheet(GUI_Style.iconButton)
        self.prevButton.setIcon(QIcon(prevIdle))
        self.prevButton.setIconSize(QSize(150, 75))

        # create next test button
        self.nextButton = QPushButton(self)
        self.nextButton.setText("")
        self.nextButton.setMaximumSize(100, 75)
        self.nextButton.setMinimumSize(100, 75)
        self.nextButton.setStyleSheet(GUI_Style.iconButton)
        self.nextButton.setIcon(QIcon(nextIdle))
        self.nextButton.setIconSize(QSize(150, 75))

        # Create section field
        self.section = QLineEdit(self)
        self.section.setReadOnly(True)
        self.section.setText("")
        self.section.setMinimumWidth(75)
        self.section.setStyleSheet(GUI_Style.section)

        # Create Test field
        self.test = QTextEdit(self)
        self.test.setReadOnly(True)
        self.test.setText("")
        self.test.setMaximumHeight(75)
        self.test.setStyleSheet(GUI_Style.testWindow)

        # Create Comment field
        self.comment = QTextEdit(self)
        self.comment.setText("")
        self.comment.setMaximumHeight(150)
        self.comment.setStyleSheet(GUI_Style.comments)

        # Create section label
        sectionLabel = QLabel(self)
        sectionLabel.setText("Section: ")
        sectionLabel.setStyleSheet(GUI_Style.label)

        # Create test label
        testabel = QLabel(self)
        testabel.setText("Test: ")
        testabel.setStyleSheet(GUI_Style.label)

        # Create min label
        minLabel = QLabel(self)
        minLabel.setText("Min")
        minLabel.setStyleSheet(GUI_Style.label)
        minLabel.setAlignment(Qt.AlignCenter)

        # Create max label
        maxLabel = QLabel(self)
        maxLabel.setText("Max")
        maxLabel.setStyleSheet(GUI_Style.label)
        maxLabel.setAlignment(Qt.AlignCenter)

        # Create unit label
        unitLabel = QLabel(self)
        unitLabel.setText("Unit")
        unitLabel.setStyleSheet(GUI_Style.label)
        unitLabel.setAlignment(Qt.AlignCenter)

        # Create Value label
        valueLabel = QLabel(self)
        valueLabel.setText("Value")
        valueLabel.setStyleSheet(GUI_Style.label)
        valueLabel.setAlignment(Qt.AlignCenter)

        # Create pass/fail label
        passFailLabel = QLabel(self)
        passFailLabel.setText("P/F")
        passFailLabel.setStyleSheet(GUI_Style.label)
        passFailLabel.setAlignment(Qt.AlignCenter)

        # Create Comments label
        commentsLabel = QLabel(self)
        commentsLabel.setText("Comments:")
        commentsLabel.setStyleSheet(GUI_Style.label)

        # Create min field
        self.minInput = QLineEdit(self)
        self.minInput.setText("")
        self.minInput.setReadOnly(True)
        self.minInput.setAlignment(Qt.AlignCenter)
        self.minInput.setMinimumSize(75,50)
        self.minInput.setMaximumSize(75,50)
        self.minInput.setStyleSheet(GUI_Style.inputBoxNonEdit)

        # Create max field
        self.maxInput = QLineEdit(self)
        self.maxInput.setText("")
        self.maxInput.setReadOnly(True)
        self.maxInput.setAlignment(Qt.AlignCenter)
        self.maxInput.setMinimumSize(75,50)
        self.maxInput.setMaximumSize(75,50)        
        self.maxInput.setStyleSheet(GUI_Style.inputBoxNonEdit)

        # Create unit field
        self.unitInput = QLineEdit(self)
        self.unitInput.setText("")
        self.unitInput.setReadOnly(True)
        self.unitInput.setAlignment(Qt.AlignCenter)
        self.unitInput.setMinimumSize(50,50)
        self.unitInput.setMaximumSize(50,50)        
        self.unitInput.setStyleSheet(GUI_Style.inputBoxNonEdit)

        # Create value field
        self.valueInput = QLineEdit(self)
        self.valueInput.setText("")
        self.valueInput.setAlignment(Qt.AlignCenter)
        self.valueInput.setMaximumWidth(50)
        self.valueInput.setMinimumSize(75,50)
        self.valueInput.setMaximumSize(75,50)   
        self.valueInput.setStyleSheet(GUI_Style.inputBox)

        # Create max field
        self.passFailInput = QLineEdit(self)
        self.passFailInput.setText("")
        self.passFailInput.setAlignment(Qt.AlignCenter)
        self.passFailInput.setMaximumWidth(50)
        self.passFailInput.setMinimumSize(50,50)
        self.passFailInput.setMaximumSize(50,50) 
        self.passFailInput.setStyleSheet(GUI_Style.passFail)

        # Create test outlone list widget
        self.testOutline = QListWidget(self)
        self.testOutline.setAcceptDrops(False)
        self.testOutline.setWordWrap(True)
        self.testOutline.setStyleSheet(GUI_Style.outlineList)
        self.testOutline.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.testOutline.setDragEnabled(False)
        self.testOutline.setMaximumWidth(100)

        # ----------------------------------
        # ------- Layout Objects -----------
        # ----------------------------------        
        # first align each label to input box
        minLay = QVBoxLayout()
        minLay.addWidget(minLabel)
        minLay.addWidget(self.minInput)
        minLay.setSpacing(5)

        maxLay = QVBoxLayout()
        maxLay.addWidget(maxLabel)
        maxLay.addWidget(self.maxInput)
        maxLay.setSpacing(5)

        unitLay = QVBoxLayout()
        unitLay.addWidget(unitLabel)
        unitLay.addWidget(self.unitInput)
        unitLay.setSpacing(5)

        valueLay = QVBoxLayout()
        valueLay.addWidget(valueLabel)
        valueLay.addWidget(self.valueInput)
        valueLay.setSpacing(5)

        passFailLay = QVBoxLayout()
        passFailLay.addWidget(passFailLabel)
        passFailLay.addWidget(self.passFailInput)
        passFailLay.setSpacing(5)

        labelLayout = QHBoxLayout()
        labelLayout.addLayout(minLay)
        labelLayout.addLayout(maxLay)
        labelLayout.addLayout(unitLay)
        labelLayout.addLayout(valueLay)
        labelLayout.addLayout(passFailLay)

        # layout previous and next buttons
        testIterateBtnLay =  QHBoxLayout()
        testIterateBtnLay.addWidget(self.prevButton)
        testIterateBtnLay.addWidget(self.nextButton)
        testIterateBtnLay.setSpacing(50)

        # layout section and test name objects
        sectionLay = QHBoxLayout()
        sectionLay.addWidget(sectionLabel)
        sectionLay.addWidget(self.section)
        sectionLay.setSpacing(5)

        testLay = QVBoxLayout()
        testLay.addWidget(testabel)
        testLay.addWidget(self.test)
        testLay.setSpacing(5)

        testSectionLay = QVBoxLayout()
        testSectionLay.addLayout(sectionLay)
        testSectionLay.addLayout(testLay)
        testSectionLay.setSpacing(10)

        # layout comment section
        commentLay = QVBoxLayout()
        commentLay.addWidget(commentsLabel)
        commentLay.addWidget(self.comment)
        commentLay.setSpacing(5)

        # final vert layout
        finalVertLayout = QVBoxLayout()
        finalVertLayout.addLayout(testSectionLay)
        finalVertLayout.addLayout(labelLayout)
        finalVertLayout.addLayout(commentLay)
        finalVertLayout.setSpacing(30)

        # final horizontal layout
        finalHorLayout = QHBoxLayout()
        finalHorLayout.addLayout(finalVertLayout)
        finalHorLayout.addWidget(self.testOutline)
        finalHorLayout.setSpacing(20)

        # final  layout
        finalLayout = QVBoxLayout()
        finalLayout.addLayout(finalHorLayout)
        finalLayout.addLayout(testIterateBtnLay)
        finalLayout.setSpacing(30)

        self.setLayout(finalLayout)
