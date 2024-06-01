import os, sys, pytube
from pytube import YouTube

class YoutubeDownloader():

    def __init__(self) -> None:
        self.DownloadTypeList = ["Video", "Audio"]
        self.ResolutionTypeList = ["Highest", "720p", "480p"]

    def Download(self, Url, DownloadType, Resolution, DownloadPath):
        if (not (DownloadType in self.DownloadTypeList)):
            return
        
        if (not (Resolution in self.ResolutionTypeList)):
            return
        
        if (not os.path.exists(DownloadPath)):
            os.mkdir(DownloadPath)

        
        try:
            youtube = YouTube(Url)

            if DownloadType == 'Video':
                if Resolution == 'Highest':
                    video = youtube.streams.get_highest_resolution()
                else:
                    video = youtube.streams.get_by_resolution(Resolution)

                video.download(DownloadPath)

            elif DownloadType == 'Audio':
                audio = youtube.streams.filter(only_audio=True)
                DownloadPath = os.path.join(DownloadPath, 'audio')

                if not os.path.exists(DownloadPath):
                    os.mkdir(DownloadPath)

                audio[0].download(DownloadPath)

        except Exception as e:
            print(e)

