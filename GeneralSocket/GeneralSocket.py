import socket, sys, threading, time, select, random

class GeneralSocket():

    def __init__(self) -> None:
        self.Socket = None
        self.ConnectionThread = None
        self.MutexLock = threading.Lock()
        self.TCBClientHandlerList = dict()
        self.UDPTargetIPList = []
        # self.ClientIPList = []
        self.SendMessageBuffer = ""
        self.SocketRunning = False

    
    def StartTCPServerThread(self, Address: tuple):
        try:
            self.Socket.bind(Address)
            self.Socket.listen()
            self.UpdateMessageBox("Start Listening")

            while(self.SocketRunning):
                Connection, Address = self.Socket.accept()

                AddressInString = str(Address)
                self.TCBClientHandlerList.update({AddressInString :{"Thread" : threading.Thread(target= self.HandleTCPAcceptedClient, args=(Connection, AddressInString), daemon= True),
                                                            "SendMessageBuffer" : ""}})
                self.TCBClientHandlerList[AddressInString]["Thread"].start()


        except Exception as e: 
            self.Disconnect()

    def HandleTCPAcceptedClient(self, Connection, Address: str):
        self.UpdateMessageBox(f"Accepted from {Address}")
        # self.UpdateTargetSender()
        try:
            with Connection:
                while (self.SocketRunning):
                    Ready = select.select([Connection], [Connection], [], 0.1)

                    for item in Ready[0]:
                        if (not (data := item.recv(4096).decode()) == ""):
                            self.UpdateMessageBox(f'{Address} Received: [{data}]')
                            
                    if (self.TCBClientHandlerList[Address]["SendMessageBuffer"] != ""):
                        for item in Ready[1]:
                            item.send(self.TCBClientHandlerList[Address]["SendMessageBuffer"].encode())
                            self.UpdateMessageBox(f'{Address} Send: [{self.TCBClientHandlerList[Address]["SendMessageBuffer"]}]')

                        self.TCBClientHandlerList[Address]["SendMessageBuffer"] = ""
        except Exception as e:
            self.UpdateMessageBox(f'Client {Address} Error: {e}')

        self.TCBClientHandlerList.pop(Address)

    def StartTCPClientThread(self, TargetAddress):
        try:
            self.Socket.connect(TargetAddress)
            while (self.SocketRunning):
                Ready = select.select([self.Socket], [self.Socket], [], 0.1)
                
                for item in Ready[0]:
                    if (not (data := item.recv(4096).decode()) == ""):
                        self.UpdateMessageBox(f'Received: [{data}]')
                    
                if (not self.SendMessageBuffer == ""):
                    # print(self.SendMessageBuffer)
                    for item in Ready[1]:
                        item.send(self.SendMessageBuffer.encode())
                        
                        self.UpdateMessageBox(f'Send: [{self.SendMessageBuffer}]')

                    self.SendMessageBuffer = ""
            
        except Exception as e:
            self.UpdateMessageBox(f'TCP client socket error: {e}')
            self.Disconnect()