from ServiceInterface import ServiceInterface
from time import sleep
import socket

class Proxy(ServiceInterface):

    def __init__(self,ip,port):
        self.ip = ip
        self.port = port

    def sendCmd(self,CommandID:int) -> None:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((self.ip,self.port))

        s.send(f"sendCmd # {CommandID}".encode())

        msg = s.recv(1024)
        print(f"[CLIENT] Ricevuto {msg.decode()}")

        s.close()

    def getCmd(self) -> int:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((self.ip,self.port))

        s.send(b"getCmd #")
        
        msg = s.recv(1024)
        print(f"[CLIENT] Ricevuto {msg.decode()}")
        
        CommandID = int(msg.decode())
        
        ack = s.recv(1024)
        print(f"[CLIENT] Ricevuto {ack.decode()}")


        s.close()

        return CommandID