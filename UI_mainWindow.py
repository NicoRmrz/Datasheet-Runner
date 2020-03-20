# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5.QtWidgets import QStatusBar, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt, QPoint, QSize

# User made files
from GUI_Stylesheets import GUI_Stylesheets
from scriptPhaseWidget import scriptPhaseWidget

GUI_Style = GUI_Stylesheets()

# Icon Image locations
Main_path = os.getcwd() + "/"
AppliedLogo = Main_path + "/icons/AppliedLogo.png"

'''
Class: Ui_MainWindow

Parameters: 
    object - base class
'''
class Ui_MainWindow(object):
    '''
    Function: __init__
		initializes when class is called
    '''
    def setupUi(self, MainWindow):

        # Main WIndow attributes
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(850, 480)
        MainWindow.setMinimumWidth(850)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setWindowIcon(QIcon(AppliedLogo))

        # create main central widget
        centralWidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(centralWidget.sizePolicy().hasHeightForWidth())
        centralWidget.setSizePolicy(sizePolicy)
        centralWidget.setTabletTracking(True)
        centralWidget.setStyleSheet(GUI_Style.mainWindow)
        centralWidget.setObjectName("centralWidget")

        # ----------------------------------
        # ------- Create Objects -----------
        # ----------------------------------
        # create logo button (my little secret)
        self.Logo = QPushButton(self)
        self.Logo.setText("")
        self.Logo.setMaximumSize(150, 75)
        self.Logo.setMinimumSize(125, 75)
        self.Logo.setStyleSheet(GUI_Style.iconButton)
        self.Logo.setIcon(QIcon(AppliedLogo))
        self.Logo.setIconSize(QSize(150, 75))

        # create main title
        titlename = QLabel(self)
        titlename.setText("Datasheet Runner")
        titlename.setStyleSheet(GUI_Style.mainTitle)

        # input serial number
        self.serNumInput = QLineEdit(self)
        self.serNumInput.setStyleSheet(GUI_Style.section)
        self.serNumInput.setReadOnly(False)

        # create first phase input script UI
        self.scriptPhaseUI = scriptPhaseWidget(self)

        # ----------------------------------
        # ------- Layout Objects -----------
        # ----------------------------------
        # layout title
        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(self.Logo)
        self.titleLayout.addWidget(titlename)
        self.titleLayout.addWidget(self.serNumInput, 1, Qt.AlignRight)
        self.titleLayout.setContentsMargins(0, 0, 10, 0)


        # Final layout
        self.FinalLayout = QVBoxLayout()
        self.FinalLayout.addLayout(self.titleLayout)
        self.FinalLayout.addWidget(self.scriptPhaseUI)
        self.FinalLayout.setSpacing(10)
        self.FinalLayout.setContentsMargins(0, 10, 10, 0)

        # set final layout
        MainWindow.setCentralWidget(centralWidget)
        centralWidget.setLayout(self.FinalLayout)
        centralWidget.isWindow()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # ----------------------------------
        # --------- StatusBar --------------
        # ----------------------------------
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet(GUI_Style.statusBarWhite)
        self.statusBar.showMessage("Starting Up... ", 4000)
        self.setStatusBar(self.statusBar)



