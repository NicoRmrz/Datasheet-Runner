from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject

# Class: dropScript
#       Window to drag and drop input scripts
# Parameters: 
#   QListWidget - inherits QListWidget attributes
class dropScript(QListWidget):
    scriptDropped = pyqtSignal(str)
    scriptname = ""

    #initializes when class is called
    def __init__(self, parent):
        super(dropScript, self).__init__(parent)
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setWordWrap(True)
        self.setSelectionMode(QListWidget.SingleSelection)

    #Pre Defined Q List widget for drag event
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    # Pre Defined Q List widget for drag move event
    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    # Pre Defined Q List widget for drop event
    def dropEvent(self, e):

        # If drag drop window has url window accepts
        if e.mimeData().hasUrls:
            e.setDropAction(Qt.CopyAction)

             # get scriptname
            for url in e.mimeData().urls():
                self.scriptname = url.toLocalFile()
                
            scriptEnding = self.scriptname.split(".")

            if scriptEnding[1] =="txt":
                 # Prints/ emit file path
                self.addItem("Input Script: " + self.scriptname)
                self.scrollToBottom()
                self.scriptDropped.emit(self.scriptname)

            else:
                self.addItem("Invalid Script with extension (" + scriptEnding[1] +")")
                self.scrollToBottom()

            e.accept()
        else:
            e.ignore()