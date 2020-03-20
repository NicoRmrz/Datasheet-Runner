import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPushButton, QDialog, QLineEdit, QLabel, QAbstractItemView, QListWidget, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject, QSize
from PyQt5.QtGui import QPixmap, QIcon

# User made files
from GUI_Stylesheets import GUI_Stylesheets
from equipmentWidget import equipmentWidget
from toolWidget import toolWidget
from materialWidget import materialWidget

GUI_Style = GUI_Stylesheets()

'''
Class: equipmentPopUpWidget
    Create widget and layout for equipment pop up
    
Parameters: 
    QDialog - inherits QDialog attributes
'''
class equipmentPopUpWidget(QDialog):

    '''
    Function: __init__
		initializes when class is called
    '''
    def __init__(self, parent):
        super(equipmentPopUpWidget, self).__init__(parent)
        self.setGeometry(50, 50, 500, 300)
        self.setMaximumSize(500, 300)
        self.setMinimumSize(500, 300)
        self.setStyleSheet(GUI_Style.mainWindow)
        self.setWindowTitle("Add Equipment")

        # ----------------------------------
        # ------- Create Objects -----------
        # ----------------------------------
        self.equipmentList = QListWidget(self)
        self.equipmentList.setAcceptDrops(False)
        self.equipmentList.setWordWrap(True)
        self.equipmentList.setStyleSheet(GUI_Style.equipmentList)
        self.equipmentList.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.equipmentList.setDragEnabled(False)
        self.equipmentList.setMinimumWidth(120)
        self.equipmentList.setMaximumWidth(120)

        # ----------------------------------
        # ------- Layout Objects -----------
        # ----------------------------------        
        self.finalLayout = QHBoxLayout()
        self.finalLayout.addWidget(self.equipmentList, 1, Qt.AlignRight)
        self.finalLayout.setSpacing(20)

        self.setLayout(self.finalLayout)

        self.equipmentWidget = None
        self.toolWidget = None
        self.materialWidget = None

    '''
    Function: updateEquipmentUI
        Function to re- layout objects for each Equipment window UI

    Parameters:
        equipType - type of equipment to be displayed [Equipment, Tools, Material]
    '''
    def switchEquipmentUI(self, equipType):

        # remove instance
        if (self.equipmentWidget != None):
            self.finalLayout.removeWidget(self.equipmentWidget)
            self.equipmentWidget.deleteLater()
            self.equipmentWidget = None

        elif (self.toolWidget != None):
            self.finalLayout.removeWidget(self.toolWidget)
            self.toolWidget.deleteLater()
            self.toolWidget = None

        elif (self.materialWidget != None):
            self.finalLayout.removeWidget(self.materialWidget)
            self.materialWidget.deleteLater()
            self.materialWidget = None

        # add in new instance
        if (equipType == "Equipment"):
            self.equipmentWidget = equipmentWidget(self)
            self.finalLayout.insertWidget(0, self.equipmentWidget)

        elif (equipType == "Tools"):
            self.toolWidget = toolWidget(self)
            self.finalLayout.insertWidget(0, self.toolWidget)

        elif (equipType == "Material"):
            self.materialWidget = materialWidget(self)
            self.finalLayout.insertWidget(0, self.materialWidget)

