from InterfacciaMagazzino import InterfacciaMagazzino
from MagazzinoImplementation import MagazzinoImplementation
from time import sleep
from threading import Thread
import socket


class Skeleton(InterfacciaMagazzino):
    
    def __init__(self):
        self.service = MagazzinoImplementation()
        
    def deposita(self, articolo, id):
        self.service.deposita(articolo,id)
        
    def preleva(self, articolo):
        return self.service.preleva(articolo)
    
    
    def runSkeleton(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind(('localhost',0))
        
        print(f"[SKELETON] In ascolto su porto: {sock.getsockname()[1]}")
        
        sock.listen(5)
        
        while True:
            connection, addr = sock.accept()
            print(f"[SKELETON] Connessione stabilita con {addr}")
            
            t = Thread(target=thd_HandleConnection,args=(self,connection))
            t.start()      


def thd_HandleConnection(skeleton:Skeleton,connection:socket.socket):
    request = connection.recv(1024)
    decoded_request = request.decode()
    print(f"[THREAD] Ricevuta stringa: {decoded_request}")
    
    ParameterList = decoded_request.split("#")
    
    if ParameterList[0].strip() == "deposita":
        skeleton.deposita(ParameterList[1],ParameterList[2])
    elif ParameterList[0].strip() == "preleva":
        ArticoloPrelevato = skeleton.preleva(ParameterList[1])
        connection.send(f"{ArticoloPrelevato}".encode())
    else:
        print(f"[THREAD] Metodo sconosciuto ricevuto: {ParameterList[0]}")
        
    sleep(1)
    
    connection.send(b"ACK")
    
    connection.close()