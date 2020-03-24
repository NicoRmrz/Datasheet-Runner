from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize

'''
Class: GUI_Stylesheets
    Stylesheet strings for each UI object
    
Parameters: 
    object - base class
'''
class GUI_Stylesheets(QObject):
    '''
    Function: __init__
		initializes when class is called
    '''
    def __init__(self):
        super(GUI_Stylesheets, self).__init__()
        
        self.mainWindow =   ("background-color: #20292F") 
        
        self.mainTitle =    ("font: bold 30px Verdana; "
                            "color: white; "
                            "background-color: rgba(18,151,147,0)"
                            )
        
        self.statusBarWhite = ("QStatusBar { background: #20292F;"
                                        "color:white; border:none;"
                                        "font: 11px Verdana; } "
                            "QStatusBar::item {border: none; "
                                "font: 11px Verdana;  "
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

        self.buttonIdle = ("font: bold 18px Verdana; "
                            "background-color: #6497b1;"
                            "border-radius: 4px")

        self.statusButtonIdle = ("font: bold 14px Verdana; "
                            "background-color: #6497b1;"
                            "border-radius: 4px; ")

        self.statusEquipButtonIdle = ("font: bold 14px Verdana; "
                            "background-color: #00A86B;"
                            "border-radius: 4px; ")

        self.beginButtonIdle = ("font: bold 18px Verdana; "
                            "background-color: rgb(39, 78, 19);"
                            "border-radius: 4px")

        self.resetButtonIdle = ("font: bold 14px Verdana; "
                            "background-color: #bd4949;"
                            "border-radius: 4px")

        self.statusButtonPressed = ("font: bold 14px Verdana; "
                            "background-color: rgb(100,100,100); "
                            "border-radius: 4px")

        self.buttonPressed = ("font: bold 18px Verdana; "
                            "background-color: rgb(100,100,100); "
                            "border-radius: 4px")
      
        self.testWindow = ("font: 18px Verdana ; "
                            "color: white; "
                            "border: none; "
                            "background-color: rgba(0,0,0,0); "
                            "padding: 4px;")
      
        self.comments = ("font: 18px Verdana ; "
                            "color: white; "
                            "background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
                                "stop: 0 #677E8C, "
                                "stop: 0.4 #59717F, "
                                "stop: 0.5 #4C6472, "
                                "stop: 1.0 #425866); "
                            "padding: 4px;")

        self.section = ("font: 18px Verdana ; "
                            "color: white; "
                            "border: none;"
                            "background-color: rgba(0,0,0,0);")
                            
        self.label = ("font: bold 20px Verdana ; "
                            "color: white; "
                            "border: none;"
                            "background-color: rgba(0,0,0,0);")
                            
        self.EquipPopUpLabel = ("font: bold 14px Verdana ; "
                            "color: white; "
                            "border: none;"
                            "background-color: rgba(0,0,0,0);")
                                                
        self.EquipInputBox = ("font: bold 14px Verdana ; "
                            "color: white; "
                            "border-radius: 2px; "
                            "border-width: 2px; "
                            "border-color: black; "                             
                            "background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
                                "stop: 0 #677E8C, "
                                "stop: 0.4 #59717F, "
                                "stop: 0.5 #4C6472, "
                                "stop: 1.0 #425866); ")
                                                
        self.calenderInput = ("QDateTimeEdit {padding-right: 15px; "
                                "border-width: 3; "
                                "color: white; "
                                "font: bold 14px Verdana ; "
                                "border-color: black; "
                                "background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
                                "stop: 0 #677E8C, "
                                "stop: 0.4 #59717F, "
                                "stop: 0.5 #4C6472, "
                                "stop: 1.0 #425866); } "
            
                                " QCalendarWidget QToolButton {height: 40px;"
                                                            "width: 125px;"
                                                            "color: white;"
                                                            "font-size: 22px;"
                                                            "icon-size: 40px, 40px;"
                                                            "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333);}"

                                "QCalendarWidget QMenu {width: 100px;"
                                    "left: 20px;"
                                    "color: white;"
                                    "font-size: 18px;"
                                    "background-color: rgb(100, 100, 100);}"

                                " QCalendarWidget QSpinBox {width: 100px; "
                                    "font-size: 16px; "
                                    "color: white; "
                                    "background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333); "
                                    "selection-background-color: rgb(136, 136, 136);"
                                    "selection-color: rgb(255, 255, 255);}"

                                "QCalendarWidget QSpinBox::up-button { subcontrol-origin: border;  subcontrol-position: top right;  width:20px; }"

                                "QCalendarWidget QSpinBox::down-button {subcontrol-origin: border; subcontrol-position: bottom right;  width:20px;}"

                                "QCalendarWidget QSpinBox::up-arrow { width:20px;  height:30px; }"

                                "QCalendarWidget QSpinBox::down-arrow { width:20px;  height:30px; }"
                                
                                # header row 6
                                "QCalendarWidget QWidget { alternate-background-color: #1c2226; }"
                                
                                # normal days 
                                "QCalendarWidget QAbstractItemView:enabled  {font-size: 16px; "
                                                                            "color: rgb(65, 134, 203);  "
                                                                            "background-color:  #20292F;  "
                                                                            "selection-background-color: rgb(65, 134, 203); "
                                                                            "selection-color: rgb(0, 255, 0); }"
                                
                                # days in other months 
                                # navigation bar 
                                "QCalendarWidget QWidget#qt_calendar_navigationbar{  background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop: 0 #cccccc, stop: 1 #333333); }"
                                "QCalendarWidget QAbstractItemView:disabled { color: rgb(100, 100, 100); }")

        self.inputBox = ("font: 18px Verdana ; "
                            "color: white; "
                            "border-radius: 2px; "
                            "border-width: 2px; "
                            "border-color: black; "                             
                            "background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
                                "stop: 0 #677E8C, "
                                "stop: 0.4 #59717F, "
                                "stop: 0.5 #4C6472, "
                                "stop: 1.0 #425866); ")
                            
        self.inputBoxNonEdit = ("font: 18px Verdana ; "
                            "color: white; "
                            "border: none;"
                             "background-color: rgba(0,0,0,0) ")
                            
        self.passFail = ("font: bold  20px Verdana ; "
                            "color: white; "
                            "border: none;"
                             "background-color: rgba(0,0,0,0) ")        
                            
        self.passFailInput = ("font: bold  20px Verdana ; "
                            "color: white; "
                             "border-radius: 2px; "
                            "border-width: 2px; "
                            "border-color: black; " 
                             "background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
                                "stop: 0 #677E8C, "
                                "stop: 0.4 #59717F, "
                                "stop: 0.5 #4C6472, "
                                "stop: 1.0 #425866); ")        
        
        self.outlineList = ("QListWidget {"
                                "font: 18px Verdana; "
                                "color: white; "
                                 "border: 1px solid;"
                                "border-color: #aeadac; }"
                            "QListWidget::item:selected {"
                                    "color: black;"
                                    "background-color: #add8e6;}")
        
        self.equipmentList = ("QListWidget {"
                                "font: 14px Verdana; "
                                "color: white; "
                                 "border: 1px solid;"
                                "border-color: #aeadac; }"
                            "QListWidget::item:selected {"
                                    "color: black;"
                                    "background-color: #add8e6;}")
         
        self.passedTest = ("font: bold  20px Verdana ; "
                            "color: white; "
                            "border: none;"
                            "border-radius: 6px;"
                            "background-color: green")    

        self.failedTest = ("font: bold  20px Verdana ; "
                            "color: white; "
                            "border: none;"
                            "border-radius: 6px;"
                             "background-color: red ")    