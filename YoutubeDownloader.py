import typing
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from pytube import YouTube
from PyQt5.QtWidgets import *
import sys,os

class YoutubeDownloader(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        
        self.DownloadType = 'Video'
        self.Resolution = 'Highest'
        self.InitUI()

    def InitUI(self):
        self.Layout = QGridLayout(self)
        RowCnt = 0

        #First Row
        self.URLLabel = QLabel("Url :",self)
        self.Layout.addWidget(self.URLLabel, RowCnt, 0, 1, 1)
        self.URLLineEdit = QPushButton("", self)
        self.Layout.addWidget(self.URLLineEdit, RowCnt, 1, 1, 3)
        RowCnt += 1

        #Second Row
        self.DownloadTypeLabel = QLabel("Download Type")
        self.Layout.addWidget(self.DownloadTypeLabel, RowCnt, 0, 1, 1)
        self.DownloadTypeComboBox = QComboBox()
        self.DownloadTypeComboBox.addItems(['Video', 'Audio'])
        self.DownloadTypeComboBox.currentIndexChanged.connect(self._DownloadTypeHandle)
        self.Layout.addWidget(self.DownloadTypeComboBox, RowCnt,1, 1, 3)
        RowCnt += 1

        #Third Row
        self.ResolutionLabel = QLabel("Resolution")
        self.Layout.addWidget(self.ResolutionLabel, RowCnt, 0, 1, 1)
        
        self.ResolutionRadioButtonGroup = QButtonGroup(self)
        self.CheckBox1 = QRadioButton('Highest')
        self.Layout.addWidget(self.CheckBox1, RowCnt, 1, 1, 1)
        self.CheckBox1.setChecked(True)
        self.CheckBox2 = QRadioButton('720p')
        self.Layout.addWidget(self.CheckBox2, RowCnt, 2, 1, 1)
        self.CheckBox3 = QRadioButton('480p')
        self.Layout.addWidget(self.CheckBox3, RowCnt, 3, 1, 1)
        self.ResolutionRadioButtonGroup.addButton(self.CheckBox1, 1)
        self.ResolutionRadioButtonGroup.addButton(self.CheckBox2, 2)
        self.ResolutionRadioButtonGroup.addButton(self.CheckBox3, 3)
        self.ResolutionRadioButtonGroup.buttonClicked.connect(self._ResolutionHandle)
        RowCnt += 1

        self.DownlaodButton = QPushButton("Download", self)
        self.DownlaodButton.clicked.connect(self._downloader)
        self.Layout.addWidget(self.DownlaodButton, RowCnt, 0, 1, 4)
        self.setLayout(self.Layout)

    def _downloader(self):
        url = self.URLLineEdit.text()
        try:
            youtube = YouTube(url)
            if self.downloadType == 'Video':
                if self.resolution == 'Highest':
                    video = youtube.streams.get_highest_resolution()
                else:
                    video = youtube.streams.get_by_resolution(self.resolution)

                if not os.path.exists('video'):
                    os.mkdir('video')

                video.download('video')

            elif self.downloadType == 'Audio':
                audio = youtube.streams.filter(only_audio=True)

                if not os.path.exists('audio'):
                    os.mkdir('audio')

                audio[0].download('audio')

        except Exception as e:
            print(e)
            QMessageBox.question(self,'Error',str(e))

    def _DownloadTypeHandle(self):
        self.DownloadType = self.DownloadTypeComboBox.currentText()

    def _ResolutionHandle(self):
        sender = self.sender()

        if sender == self.ResolutionRadioButtonGroup:
            self.Resolution = self.ResolutionRadioButtonGroup.checkedButton().text()
            print(self.Resolution)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    container = YoutubeDownloader(None)
    container.setGeometry(1,90,500,300)
    container.show()
    sys.exit(app.exec_())
