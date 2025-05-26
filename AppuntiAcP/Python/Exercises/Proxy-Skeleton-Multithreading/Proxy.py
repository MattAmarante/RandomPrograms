from InterfacciaMagazzino import InterfacciaMagazzino
import socket


class Proxy(InterfacciaMagazzino):
    
    def __init__(self,port):
        self.port = int(port)
    
    def preleva(self, articolo):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect(('localhost',self.port))
        
        print(f"[PROXY] Invio richiesta di prelevazione di {articolo}")
        sock.send(f"preleva # {articolo}".encode())
        
        ArticoloPrelevato = sock.recv(1024)
        ArticoloPrelevato = ArticoloPrelevato.decode()
        sock.recv(1024) # Ricezione ACK
        
        sock.close()
        
        return ArticoloPrelevato
        
    
    def deposita(self, articolo, id):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect(('localhost',self.port))
        
        print(f"[PROXY] Invio richiesta di deposito di {articolo},ID:{id}")
        sock.send(f"deposita # {articolo} # {id}".encode())
        
        sock.recv(1024) # Ricezione ACK
        
        sock.close()