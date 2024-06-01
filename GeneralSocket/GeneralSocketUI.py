import socket, threading

class GeneralSocket():

    def __init__(self) -> None:
        self.Socket = None
        self.ConnectionThread = None
        self.MutexLock = threading.Lock()
        self.TCBClientHandlerList = dict()
        self.UDPTargetIPList = []
        # self.ClientIPList = []
        self.SendMessageBuffer = ""
        self.MessageBoxContent = "App Start\n"
        self.SocketRunning = False


    def Start():
        pass

    def Send(Message):
        pass