import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QDialog, QLineEdit, QLabel, QAbstractItemView, QListWidget, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject, QSize
from PyQt5.QtGui import QPixmap, QIcon

# User made files
from GUI_Stylesheets import GUI_Stylesheets

GUI_Style = GUI_Stylesheets()

'''
Class: toolWidget
    Create widget and layout for tools in equipment pop up
    
Parameters: 
    QWidget - inherits QWidget attributes
'''
class toolWidget(QWidget):

    '''
    Function: __init__
		initializes when class is called
    '''
    def __init__(self, parent):
        super(toolWidget, self).__init__(parent)

        # ----------------------------------
        # ------- Create Objects -----------
        # ----------------------------------
        versionLabel = QLabel(self)
        versionLabel.setText("Version:")
        versionLabel.setStyleSheet(GUI_Style.EquipPopUpLabel)
        versionLabel.setAlignment(Qt.AlignCenter)

        self.versionInput = QLineEdit(self)
        self.versionInput.setText("")
        self.versionInput.setMinimumSize(175, 25)
        self.versionInput.setMaximumSize(175, 25)
        self.versionInput.setStyleSheet(GUI_Style.EquipInputBox)

        # ----------------------------------
        # ------- Layout Objects -----------
        # ----------------------------------        
        finalLayout = QVBoxLayout()
        finalLayout.addWidget(versionLabel)
        finalLayout.addWidget(self.versionInput, 1, Qt.AlignTop)
        finalLayout.setSpacing(15)
        finalLayout.setContentsMargins(90, 50, 0, 0)

        self.setLayout(finalLayout)
