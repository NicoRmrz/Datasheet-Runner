import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QDialog, QLineEdit, QLabel, QAbstractItemView, QCalendarWidget, QListWidget, QWidget, QHBoxLayout, QVBoxLayout, QDateTimeEdit
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject, QSize, QDate
from PyQt5.QtGui import QPixmap, QIcon

# User made files
from GUI_Stylesheets import GUI_Stylesheets

GUI_Style = GUI_Stylesheets()

'''
Class: equipmentWidget
    Create widget and layout for tools in equipment pop up
    
Parameters: 
    QWidget - inherits QWidget attributes
'''
class equipmentWidget(QWidget):

    '''
    Function: __init__
		initializes when class is called
    '''
    def __init__(self, parent):
        super(equipmentWidget, self).__init__(parent)

        # ----------------------------------
        # ------- Create Objects -----------
        # ----------------------------------
        modelLabel = QLabel(self)
        modelLabel.setText("Model:")
        modelLabel.setStyleSheet(GUI_Style.EquipPopUpLabel)
        modelLabel.setAlignment(Qt.AlignRight)

        self.modelInput = QLineEdit(self)
        self.modelInput.setText("")
        self.modelInput.setMinimumSize(150, 25)
        self.modelInput.setMaximumSize(175, 25)
        self.modelInput.setStyleSheet(GUI_Style.EquipInputBox)

        equipmentID = QLabel(self)
        equipmentID.setText("Equipment ID #")
        equipmentID.setStyleSheet(GUI_Style.EquipPopUpLabel)
        equipmentID.setAlignment(Qt.AlignRight)

        self.equipmentIDInput = QLineEdit(self)
        self.equipmentIDInput.setText("")
        self.equipmentIDInput.setMinimumSize(150, 25)
        self.equipmentIDInput.setMaximumSize(175, 25)
        self.equipmentIDInput.setStyleSheet(GUI_Style.EquipInputBox)

        calibrationID = QLabel(self)
        calibrationID.setText("Calibration ID #")
        calibrationID.setStyleSheet(GUI_Style.EquipPopUpLabel)
        calibrationID.setAlignment(Qt.AlignRight)

        self.calibrationIDInput = QLineEdit(self)
        self.calibrationIDInput.setText("")
        self.calibrationIDInput.setMinimumSize(150, 25)
        self.calibrationIDInput.setMaximumSize(175, 25)
        self.calibrationIDInput.setStyleSheet(GUI_Style.EquipInputBox)

        calDueDate = QLabel(self)
        calDueDate.setText("Cal. Due Date:")
        calDueDate.setStyleSheet(GUI_Style.EquipPopUpLabel)
        calDueDate.setAlignment(Qt.AlignRight)

        calender = QCalendarWidget(self)
        calender.setGridVisible(True)
        calender.setStyleSheet(GUI_Style.calenderInput)

        self.calDueDateInput = QDateTimeEdit(self)
        self.calDueDateInput.setMinimumSize(150, 25)
        self.calDueDateInput.setMaximumSize(175, 25)
        self.calDueDateInput.setCalendarPopup(True)
        self.calDueDateInput.setCalendarWidget(calender)
        self.calDueDateInput.setDate(QDate.currentDate())
        self.calDueDateInput.setMinimumDate(QDate.currentDate().addDays(-500))
        self.calDueDateInput.setMaximumDate(QDate.currentDate().addDays(1000))
        self.calDueDateInput.setStyleSheet(GUI_Style.calenderInput)
        self.calDueDateInput.setDisplayFormat("MMM d, yyyy")

        # ----------------------------------
        # ------- Layout Objects -----------
        # ----------------------------------    
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(modelLabel)
        leftLayout.addWidget(equipmentID)
        leftLayout.addWidget(calibrationID)
        leftLayout.addWidget(calDueDate)
        leftLayout.setSpacing(10)
        leftLayout.setContentsMargins(0, 25, 0, 0)

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.modelInput)
        rightLayout.addWidget(self.equipmentIDInput)
        rightLayout.addWidget(self.calibrationIDInput)
        rightLayout.addWidget(self.calDueDateInput)
        # rightLayout.addWidget(self.calInput)
        rightLayout.setSpacing(10)

        finalLayout = QHBoxLayout()
        finalLayout.addLayout(leftLayout)
        finalLayout.addLayout(rightLayout)
        finalLayout.setSpacing(25)
        finalLayout.setContentsMargins(20, 20, 0, 0)

        self.setLayout(finalLayout)
