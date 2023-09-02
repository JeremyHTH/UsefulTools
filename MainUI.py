import sys,time,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtGui

from YoutubeDownloader import YoutubeDownloader

class CenterWidget(QWidget):
    def __init__(self, StatusBar):
        super().__init__()

        self.StatusBar = StatusBar
        self.init_UI()
        

    def init_UI(self):
        self.layout = QGridLayout(self)

        self.CurrentWidget = YoutubeDownloader(self)
        self.layout.addWidget(self.CurrentWidget,0,0,1,1)
        self.StatusBar.showMessage('Youtube Downloader')
        
        self.setLayout(self.layout)

    
    def close(self) -> bool:
        return super().close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(1,90,800,600)
        self.setWindowTitle("Useful tools")
        self.status = QStatusBar(self)
        self.status.showMessage("Welcome")
        self.setStatusBar(self.status)
        
        self.CenterWid = CenterWidget(self.status)
        self.setCentralWidget(self.CenterWid)

        self.setStyle(QStyleFactory.create('fusion'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    container = MainWindow()

    container.show()
    sys.exit(app.exec_())