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
        toolLabel = QLabel(self)
        toolLabel.setText("Tool:")
        toolLabel.setStyleSheet(GUI_Style.EquipPopUpLabel)

        # ----------------------------------
        # ------- Layout Objects -----------
        # ----------------------------------        
        self.finalLayout = QHBoxLayout()
        self.finalLayout.addWidget(toolLabel)
        self.finalLayout.setSpacing(0)

        self.setLayout(self.finalLayout)
