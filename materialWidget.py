import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QDialog, QLineEdit, QLabel, QAbstractItemView, QListWidget, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject, QSize
from PyQt5.QtGui import QPixmap, QIcon

# User made files
from GUI_Stylesheets import GUI_Stylesheets

GUI_Style = GUI_Stylesheets()

'''
Class: materialWidget
    Create widget and layout for materials in equipment pop up
    
Parameters: 
    QWidget - inherits QWidget attributes
'''
class materialWidget(QWidget):

    '''
    Function: __init__
		initializes when class is called
    '''
    def __init__(self, parent):
        super(materialWidget, self).__init__(parent)

        # ----------------------------------
        # ------- Create Objects -----------
        # ----------------------------------
        serNumLabel = QLabel(self)
        serNumLabel.setText("Serial Number: ")
        serNumLabel.setStyleSheet(GUI_Style.EquipPopUpLabel)
        serNumLabel.setAlignment(Qt.AlignRight)

        self.serialInput = QLineEdit(self)
        self.serialInput.setText("")
        self.serialInput.setMinimumSize(150, 25)
        self.serialInput.setMaximumSize(175, 25)
        self.serialInput.setStyleSheet(GUI_Style.EquipInputBox)

        revisionLabel = QLabel(self)
        revisionLabel.setText("Revision: ")
        revisionLabel.setStyleSheet(GUI_Style.EquipPopUpLabel)
        revisionLabel.setAlignment(Qt.AlignRight)

        self.revisionInput = QLineEdit(self)
        self.revisionInput.setText("")
        self.revisionInput.setMinimumSize(150, 25)
        self.revisionInput.setMaximumSize(175, 25)
        self.revisionInput.setStyleSheet(GUI_Style.EquipInputBox)

        firmwareLabel = QLabel(self)
        firmwareLabel.setText("Firmware Version: ")
        firmwareLabel.setStyleSheet(GUI_Style.EquipPopUpLabel)
        firmwareLabel.setAlignment(Qt.AlignRight)

        self.firmwareInput = QLineEdit(self)
        self.firmwareInput.setText("")
        self.firmwareInput.setMinimumSize(150, 25)
        self.firmwareInput.setMaximumSize(175, 25)
        self.firmwareInput.setStyleSheet(GUI_Style.EquipInputBox)

        softwareLabel = QLabel(self)
        softwareLabel.setText("Software Version: ")
        softwareLabel.setStyleSheet(GUI_Style.EquipPopUpLabel)
        softwareLabel.setAlignment(Qt.AlignRight)

        self.softwareInput = QLineEdit(self)
        self.softwareInput.setText("")
        self.softwareInput.setMinimumSize(150, 25)
        self.softwareInput.setMaximumSize(175, 25)
        self.softwareInput.setStyleSheet(GUI_Style.EquipInputBox)

        # ----------------------------------
        # ------- Layout Objects -----------
        # ----------------------------------        
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(serNumLabel)
        leftLayout.addWidget(revisionLabel)
        leftLayout.addWidget(firmwareLabel)
        leftLayout.addWidget(softwareLabel)
        leftLayout.setSpacing(10)
        leftLayout.setContentsMargins(0, 25, 0, 0)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.serialInput)
        rightLayout.addWidget(self.revisionInput)
        rightLayout.addWidget(self.firmwareInput)
        rightLayout.addWidget(self.softwareInput)
        rightLayout.setSpacing(10)
        
        finalLayout = QHBoxLayout()
        finalLayout.addLayout(leftLayout)
        finalLayout.addLayout(rightLayout)
        finalLayout.setSpacing(25)
        finalLayout.setContentsMargins(20, 20, 0, 0)

        self.setLayout(finalLayout)
