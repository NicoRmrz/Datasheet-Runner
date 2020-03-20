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
        pass

        # ----------------------------------
        # ------- Create Objects -----------
        # ----------------------------------


        # ----------------------------------
        # ------- Layout Objects -----------
        # ----------------------------------        
        # self.finalLayout = QHBoxLayout()
        # self.finalLayout.addWidget()
        # self.finalLayout.setSpacing()

        # self.setLayout(self.finalLayout)
