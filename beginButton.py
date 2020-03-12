# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject

# Class: GUI_SbeginButtontylesheets
# Parameters: 
#   QPushButton - inherits QPushButton class
class beginButton(QPushButton):
    removeInstance = pyqtSignal()

    # Initializes the necessary objects into the button class for control
    def __init__(self, window, text, dropWindow):
        super(beginButton, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.setMaximumSize(150, 50)
        self.setMinimumSize(125, 50)
        self.dropWindow = dropWindow

        # Connect signals to slots
        self.pressed.connect(self.On_Click)
        self.released.connect(self.Un_Click)

   # Function: On_Click
    # 		Slot to handle button click
    def On_Click(self):
        pass

    # Function: Un_Click
    # 		Slot to handle button released and move to starting test proced
    def Un_Click(self):
        # to remove widget
        self.removeInstance.emit()
        self.dropWindow.deleteLater()
        self.deleteLater()
        self.dropWindow = None
        self = None
    
    