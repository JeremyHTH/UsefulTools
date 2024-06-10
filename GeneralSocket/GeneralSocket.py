import socket, sys, threading, time, select, random

class GeneralSocket():

    def __init__(self) -> None:
        self.Socket = None
        self.ConnectionThread = None
        self.SystemLogBufferMutexLock = threading.Lock()
        self.SystemLogBuffer = []

        self.TCBClientHandlerList = dict()
        self.UDPTargetIPList = []
        # self.ClientIPList = []
        self.ReceiveMessageBufferMutexLock = threading.Lock()
        self.ReceiveMessageBuffer = []

        self.SendMessageBufferMutexLock = threading.Lock()
        self.SendMessageBuffer = []

        self.SocketRunning = False
    
    def StartTCPServerThread(self, Address: tuple):
        try:
            self.Socket.bind(Address)
            self.Socket.listen()

            while(self.SocketRunning):
                Connection, Address = self.Socket.accept()

                AddressInString = str(Address)
                self.TCBClientHandlerList.update({AddressInString :{"Thread" : threading.Thread(target= self.HandleTCPAcceptedClient, args=(Connection, AddressInString), daemon= True), "Mutex" : threading.Lock(), "SendMessageBuffer": []}})
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
                            # self.UpdateMessageBox(f'{Address} Received: [{data}]')
                            pass
                            
                    if (self.TCBClientHandlerList[Address]["SendMessageBuffer"] != ""):
                        for item in Ready[1]:
                            item.send(self.TCBClientHandlerList[Address]["SendMessageBuffer"].encode())
                            self.UpdateMessageBox(f'{Address} Send: [{self.TCBClientHandlerList[Address]["SendMessageBuffer"]}]')

                        self.TCBClientHandlerList[Address]["SendMessageBuffer"] = ""
        except Exception as e:
            print(e)
            
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

    def Start(self, Protocol: str, SocketType: str):

        if (self.ConnectionThread == None):
            if (Protocol == 'TCP'):
                self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                if (SocketType == 'Server'):
                    self.ConnectionThread = threading.Thread(target= self.StartTCPServerThread, args=(), daemon= True)
                elif (SocketType == 'Client'):
                    self.ConnectionThread = threading.Thread(target= self.StartTCPClientThread, args=(), daemon= True)

            # elif (Protocol == 'UDP'):
            #     self.Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            #     if (SocketType == 'Server'):
            #         self.ConnectionThread = threading.Thread(target= self.StartUDPServerThread, args=(), daemon= True)
            #     elif (SocketType == 'Client'):
            #         self.ConnectionThread = threading.Thread(target= self.StartUDPClientThread, args=(), daemon= True)

            self.SocketRunning = True
            self.ConnectionThread.start()


    def Terminate(self):
        if (not self.ConnectionThread == None):
            self.SocketRunning = False
            if (self.Socket != None):
                try:
                    self.Socket.shutdown(socket.SHUT_RDWR)
                except Exception as e:
                    pass
                self.Socket.close()
            self.Socket = None
            self.ConnectionThread = None
            
            self.TCBClientHandlerList.clear()
            self.UDPTargetIPList.clear()            

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("ProtocolType")
    parser.add_argument("SocketType")
    args = parser.parse_args()

    if (not (args.ProtocolType in ("TCP", "UDP"))):
        print("Protocol Error")
        return
        
    
    if (not (args.SocketType in ("Server", "Client"))):
        print("Socket Error")
        return
    
    CurrentSocket = GeneralSocket()

    CurrentSocket.Start(args.ProtocolType, args.SocketType)
    

if __name__ == '__main__':
    main()