from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QTextEdit, QAbstractScrollArea,  QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject

# User made files
from GUI_Stylesheets import GUI_Stylesheets
from dropScript import dropScript

GUI_Style = GUI_Stylesheets()

'''
Class: scriptPhaseWidget
    Create widget and layout for testing phase

Parameters: 
    QListWidget - inherits QWidget attributes
'''
class scriptPhaseWidget(QWidget):
    removeInstance = pyqtSignal()
    
    '''
    Function: __init__
		initializes when class is called
    '''
    def __init__(self, parent):
        super(scriptPhaseWidget, self).__init__(parent)

        # ----------------------------------
        # ------- Create Objects -----------
        # ----------------------------------
        # create drag and drop script window
        self.dropWindow = dropScript(self)

        # create restore session button
        self.restoreSeshBtn = QPushButton(self)
        self.restoreSeshBtn.setText("Restore Session")
        self.restoreSeshBtn.setMaximumSize(200, 50)
        self.restoreSeshBtn.setMinimumSize(150, 50)
        self.restoreSeshBtn.setStyleSheet(GUI_Style.buttonIdle)

        # create begin button
        self.beginBtn = QPushButton(self)
        self.beginBtn.setText("Begin")
        self.beginBtn.setMaximumSize(200, 50)
        self.beginBtn.setMinimumSize(150, 50)
        self.beginBtn.setEnabled(False)
        self.beginBtn.setStyleSheet(GUI_Style.beginButtonIdle)

        # create Data Analysis button
        self.dataAnalysisBtn = QPushButton(self)
        self.dataAnalysisBtn.setText("Data Analysis")
        self.dataAnalysisBtn.setMaximumSize(200, 50)
        self.dataAnalysisBtn.setMinimumSize(150, 50)
        self.dataAnalysisBtn.setStyleSheet(GUI_Style.buttonIdle)

        # ----------------------------------
        # ------- Layout Objects -----------
        # ----------------------------------          
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.beginBtn)
        buttonLayout.addWidget(self.restoreSeshBtn)
        buttonLayout.addWidget(self.dataAnalysisBtn)
        buttonLayout.setSpacing(50)

        FinalLayout = QVBoxLayout()
        FinalLayout.addWidget(self.dropWindow)
        FinalLayout.addLayout(buttonLayout)
        FinalLayout.setSpacing(25)

        self.setLayout(FinalLayout)

        # Connect signals to slots
        self.beginBtn.pressed.connect(self.beginButton_Pressed)
        self.beginBtn.released.connect(self.beginButton_Released)
        self.restoreSeshBtn.pressed.connect(self.restoreButton_Pressed)
        self.restoreSeshBtn.released.connect(self.restoreButton_Released)
        self.dropWindow.enableBtn.connect(self.buttonEnable)

    # ----------------------------------
    # ------- Restore Session ----------
    # ---------------------------------- 
    '''
    Function: restoreButton_Pressed
        Slot to handle button click
    '''
    def restoreButton_Pressed(self):
        self.restoreSeshBtn.setStyleSheet(GUI_Style.buttonPressed)

    '''
    Function: beginButton_Released
        Slot to handle button released
    '''
    def restoreButton_Released(self):
        self.restoreSeshBtn.setStyleSheet(GUI_Style.buttonIdle)

    # ----------------------------------
    # ------- Begin Session ------------
    # ---------------------------------- 
    ''' 
    Function: beginButton_Pressed
        Slot to handle button click
    '''
    def beginButton_Pressed(self):
        self.beginBtn.setStyleSheet(GUI_Style.buttonPressed)

    '''
    Function: beginButton_Released
        Slot to handle button released to re layout UI for testing phase
    '''
    def beginButton_Released(self):
        self.beginBtn.setStyleSheet(GUI_Style.buttonIdle)

        # to remove widget
        self.removeInstance.emit()

    '''
    Function: buttonEnable
        Set button enable state
        
	Parameters: 
	  	state - button enable status
    '''
    def buttonEnable(self, state):
        self.beginBtn.setEnabled(state)
