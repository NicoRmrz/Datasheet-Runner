# -*- coding: utf-8 -*-
import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow

#imports from user made file
from GUI_Stylesheets import GUI_Stylesheets
from UI_mainWindow import Ui_MainWindow
from dropScript import dropScript

GUI_Style = GUI_Stylesheets()

# Current version of application - Update for new builds
appVersion = "1.0"      # Update version

# Icon Image locations
Main_path = os.getcwd() + "/"
AppliedLogo = Main_path + "/icons/AppliedLogo.png"

DATASHEET_DICT = {}

# Class: MainWindow
# Parameters: 
#   QMainWindow - inherits QMainWindow attributes
#   Ui_MainWindow - all objects made from UI_Mainwindow are brought to the MainWindow class
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Protocol Data Entry v" + appVersion)
        self.setWindowIcon(QIcon(AppliedLogo))

        # Connect signals to slots
        self.Logo.clicked.connect(self.On_Click)

    @pyqtSlot()
    # Function: sendStatusMessage
    # 		Slot to send a status bar message
    # Parameters: 
    #   	message -  message to show on status bar
    #   	time -  time for message to show
    def sendStatusMessage(self, message, time):
        self.statusBar.showMessage(message, time)

    # Function: On_Click
    # 		Slot to handle secret button click
    def On_Click(self):
        self.dropWindow = dropScript(self)
        self.FinalLayout.addWidget(self.dropWindow)
        # Connect signals to slots
        self.dropWindow.removeInstance.connect(self.removeDropWindow)

    # Function: removeDropWindow
    # 		Slot to handle removing the drag and drop window for the next phase
    def removeDropWindow(self):
        self.FinalLayout.removeWidget(self.dropWindow)

    # ------------------------------------------------------------------
    # ----------- Close All Threads at app closure ---------------------
    # ------------------------------------------------------------------             
    # Stop all threads when GUI is closed
    def closeEvent(self, *args, **kwargs):
        self.dropWindow.parseThread.terminate
        self.dropWindow.parseThread.wait(100)        
        sys.exit(0);