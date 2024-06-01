import socket, sys, threading, time, select
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QBrush, QColor
from PyQt5 import QtGui

from YoutubeDownloader import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
 

        self.ToolsDict = { 'Youtube DownLoader' : YoutubeDownloaderUI}


        self.CenterWid = self.ToolsDict['Youtube DownLoader'](self)
        self.setGeometry(1,90,800,400)
        self.setWindowTitle("Control Center")

        self.CreateMenuBar()

        self.setCentralWidget(self.CenterWid)
        self.status = QStatusBar(self)
        self.status.showMessage("Welcome")
        self.setStatusBar(self.status)

        self.setWindowIcon(QtGui.QIcon("Image\logo.png"))
        self.setStyle(QStyleFactory.create('fusion'))
        self.setStyleSheet(self.LoadStyle())
    
    def CreateMenuBar(self):
        MenuBar = QMenuBar(self)

        ToolsMenu = QMenu("&Tools", self)

        # self.ContourMoveWidgetAction = QAction("Contour Move", self)
        # self.ContourMoveWidgetAction.triggered.connect(self.ChangeCenterWidget)
        # ToolsMenu.addAction(self.ContourMoveWidgetAction)

        # self.GeneralSocketWidgetAction = QAction("General Socket", self)
        # self.GeneralSocketWidgetAction.triggered.connect(self.ChangeCenterWidget)
        # ToolsMenu.addAction(self.GeneralSocketWidgetAction)

        for index, key in enumerate(self.ToolsDict.keys()):
                
            Action = QAction(key, self)
            if (index < 9):
                Action.setShortcut(f'Ctrl+{index + 1}')
            Action.triggered.connect(self.ChangeCenterWidget)
            ToolsMenu.addAction(Action)

        MenuBar.addMenu(ToolsMenu)

        self.setMenuBar(MenuBar)
    
    def ChangeCenterWidget(self):
        sender = self.sender()

        if (sender.text() in self.ToolsDict.keys()):
            self.CenterWid = self.ToolsDict[sender.text()](self)
            self.setCentralWidget(self.CenterWid)
    


    def LoadStyle(self):
        data = ""
        try:
            with open('Sytle.css','r') as f: 
                data = f.read()
        except Exception as e:
            print(e.args)
            # QMessageBox.question(self,'Error',str(e))
        return data
    
    def close(self) -> bool:
        self.CenterWid.close()
        return super().close()
    


if __name__ == '__main__':
    import platform
    if (platform.system() == 'Window'):
        import ctypes
        myappid = 'MyApp.Ver1.0' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    container = MainWindow()

    container.show()
    sys.exit(app.exec_())