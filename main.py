from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow

#Runs python application
if __name__== "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show() 
    sys.exit(app.exec_())
    