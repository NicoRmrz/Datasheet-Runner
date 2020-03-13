import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QTextEdit, QAbstractScrollArea,  QGroupBox, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject, QSize
from PyQt5.QtGui import QPixmap, QIcon

# User made files
from GUI_Stylesheets import GUI_Stylesheets

GUI_Style = GUI_Stylesheets()

# Icon Image locations
Main_path = os.getcwd() + "/"
nextIdle = Main_path + "/icons/nextIdle.png"
prevIdle = Main_path + "/icons/previousIdle.png"

# Class: testPhaseWidget
#       Create widget and layout for testing phase
# Parameters: 
#   QListWidget - inherits QWidget attributes
class testPhaseWidget(QWidget):

    #initializes when class is called
    def __init__(self, parent):
        super(testPhaseWidget, self).__init__(parent)

        # create reset phase button
        self.resetButton = QPushButton(self)
        self.resetButton.setText("Reset")
        self.resetButton.setMaximumSize(75, 30)
        self.resetButton.setMinimumSize(75, 30)
        self.resetButton.setStyleSheet(GUI_Style.resetButtonIdle)

        # create save session button
        self.saveButton = QPushButton(self)
        self.saveButton.setText("Save")
        self.saveButton.setMaximumSize(75, 30)
        self.saveButton.setMinimumSize(75, 30)
        self.saveButton.setStyleSheet(GUI_Style.buttonIdle)

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
        self.section.setText("Section: ")
        self.section.setMinimumWidth(75)
        self.section.setStyleSheet(GUI_Style.section)

        # Create Test field
        self.test = QTextEdit(self)
        self.test.setReadOnly(True)
        self.test.setText("Test: ")
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

        # Create max label
        maxLabel = QLabel(self)
        maxLabel.setText("Max")
        maxLabel.setStyleSheet(GUI_Style.label)

        # Create unit label
        unitLabel = QLabel(self)
        unitLabel.setText("Unit")
        unitLabel.setStyleSheet(GUI_Style.label)

        # Create Value label
        valueLabel = QLabel(self)
        valueLabel.setText("Value")
        valueLabel.setStyleSheet(GUI_Style.label)

        # Create pass/fail label
        passFailLabel = QLabel(self)
        passFailLabel.setText("P/F")
        passFailLabel.setStyleSheet(GUI_Style.label)

        # Create Comments label
        commentsLabel = QLabel(self)
        commentsLabel.setText("Comments:")
        commentsLabel.setStyleSheet(GUI_Style.label)

        # Create min field
        self.minInput = QLineEdit(self)
        self.minInput.setText("rr")
        self.minInput.setReadOnly(True)
        self.minInput.setAlignment(Qt.AlignCenter)
        self.minInput.setMinimumSize(50,50)
        self.minInput.setMaximumSize(50,50)
        self.minInput.setStyleSheet(GUI_Style.inputBoxNonEdit)

        # Create max field
        self.maxInput = QLineEdit(self)
        self.maxInput.setText("maxxia")
        self.maxInput.setReadOnly(True)
        self.maxInput.setAlignment(Qt.AlignCenter)
        self.maxInput.setMinimumSize(50,50)
        self.maxInput.setMaximumSize(50,50)        
        self.maxInput.setStyleSheet(GUI_Style.inputBoxNonEdit)

        # Create unit field
        self.unitInput = QLineEdit(self)
        self.unitInput.setText("mV")
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
        self.passFailInput.setReadOnly(True)
        self.passFailInput.setAlignment(Qt.AlignCenter)
        self.passFailInput.setMaximumWidth(50)
        self.passFailInput.setMinimumSize(50,50)
        self.passFailInput.setMaximumSize(50,50) 
        self.passFailInput.setStyleSheet(GUI_Style.passFail)

        # Layout Widget
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

        # layout save and reset buttons
        self.saveResetLay = QVBoxLayout()
        self.saveResetLay.addWidget(self.saveButton, 0, Qt.AlignRight)
        self.saveResetLay.addWidget(self.resetButton, 0, Qt.AlignRight)
        self.saveResetLay.setSpacing(10)

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

        # final layout
        finalLayout = QVBoxLayout()
        finalLayout.addLayout(testSectionLay)
        finalLayout.addLayout(labelLayout)
        finalLayout.addLayout(commentLay)
        finalLayout.addLayout(testIterateBtnLay)
        finalLayout.setSpacing(30)

        self.setLayout(finalLayout)
