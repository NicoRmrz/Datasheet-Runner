from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize

# Class: GUI_Stylesheets
#   Stylesheet strings for each UI object
# Parameters: 
#   object - base class
class GUI_Stylesheets(QObject):
    def __init__(self):
        super(GUI_Stylesheets, self).__init__()
        
        self.mainWindow =   ("background-color: #20292F") 
        
        self.mainTitle =    ("font: bold 30px Verdana; "
                            "color: white; "
                            "background-color: rgba(18,151,147,0)"
                            )
        
        self.statusBarWhite = ("QStatusBar { background: #20292F;"
                                        "color:white;} "
                                        "font: 20 px Verdana;  "
                            "QStatusBar::item {border: 1px solid #313335; "
                                "font: 20 px Verdana;  "
                                "border-radius: 3px; }"
                            )
        
        self.statusBarRed = ("QStatusBar {color:red;} ")
                            
        self.iconButton =  ("font: bold 12px Verdana; "
                            "background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
                                "stop:0 rgba(242, 242, 242, 0), "
                                "stop:1 rgba(255,255,255,0)); "
                                "border: none; "
                            )
                            
        self.dropWindow = ("font: 14px Verdana ; "
                            "color: white; "
                            "background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
                                "stop: 0 #677E8C, "
                                "stop: 0.4 #59717F, "
                                "stop: 0.5 #4C6472, "
                                "stop: 1.0 #425866); "
                            "border-style: dashed; "
                            "border-radius: 4px; "
                            "border-width: 6px; "
                            "border-color: black; "
                            "padding: 4px;")
