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
from parserThread import parserThread

GUI_Style = GUI_Stylesheets()

# Current version of application - Update for new builds
appVersion = "1.0"      # Update version

# Icon Image locations
Main_path = os.getcwd() + "/"
AppliedLogo = Main_path + "/icons/AppliedLogo.png"

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

        # instantiate threads
        self.parseThread = parserThread()


        
        
        # Connect signals to slots
        self.dropWindow.scriptDropped.connect(self.receiveScript)


    @pyqtSlot()
    def sendStatusMessage(self, message, time):
        self.statusBar.showMessage(message, time)

    def receiveScript(self, script):
        self.parseThread.setScriptToParse(script, True)
        self.parseThread.start()


    # ------------------------------------------------------------------
    # ----------- Close All Threads at app closure ---------------------
    # ------------------------------------------------------------------             
    # Stop all threads when GUI is closed
    def closeEvent(self, *args, **kwargs):
        self.parseThread.terminate
        self.parseThread.wait(100)        
    
        sys.exit(0);