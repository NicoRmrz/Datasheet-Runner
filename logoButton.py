# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from PyQt5.QtWidgets import QPushButton

## This is the class for push buttons from the Pyqt 5 framework
class logoButton(QPushButton):

    # Initializes the necessary objects into the button class for control
    def __init__(self, window, text):
        super(logoButton, self).__init__()
        self.setText(text)
        self.setParent(window)

    
    # Function call for the click event
    def On_Click(self):
        pass

    # Function call for the Un_click event
    def Un_Click(self):
        pass
    