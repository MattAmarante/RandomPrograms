from ServiceInterface import ServiceInterface
from multiprocessing import Queue,Process
from time import sleep
import socket

class Skeleton(ServiceInterface):
    
    def __init__(self,ip,port,Disp):
        self.Disp:Dispatcher = Disp

        self.ip = ip
        self.port = port
    
    def sendCmd(self,CommandID:int) -> None:
        print("[SKELETON] Sono nel metodo sendCmd.")
        self.Disp.sendCmd(CommandID)

    def getCmd(self) -> int:
        print("[SKELETON] Sono nel metodo getCmd")
        return self.Disp.getCmd()

    def runSkeleton(self) -> None:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((self.ip,self.port))
        print(f"[DISPATCHER] In ascolto su:\n" +
              f"IP: {sock.getsockname()[0]}\n" +
              f"Porto: {sock.getsockname()[1]}")

        sock.listen(5)

        while True:

            conn,addr = sock.accept()
            print(f"[SKELETON] Stabilita connessione con {addr}")
            
            p = Process(target=prc_HandleConnection,args=(conn,self))
            p.start()

            conn.close()


def prc_HandleConnection(conn:socket.socket,Skel:Skeleton):
    msg = conn.recv(1024)
    decoded_msg = msg.decode()

    # Formato <comando> # <parametro1>,<parametro2> ... etc.
    param_list = decoded_msg.split("#")

    if param_list[0].strip() == "sendCmd":
        print(f"[PROCESSO] Invoco sendCmd con parametro {param_list[1]}")
        Skel.sendCmd(int(param_list[1]))
    elif param_list[0].strip() == "getCmd":
        print("[PROCESSO] Invoco getCmd")
        cmd = str(Skel.getCmd())

        print(f"[PROCESSO] Invio {cmd} al Dispatcher")
        conn.send(cmd.encode())

    sleep(1)
    conn.send("ACK".encode())
    
    conn.close()


class Dispatcher(Skeleton):
    
    def __init__(self, queue = Queue(5)):
        self.queue = queue
    
    def sendCmd(self,CommandID:int) -> None:
        print(f"[DISPATCHER] Inserisco {CommandID}")
        self.queue.put(CommandID)

    def getCmd(self) -> int:
        print(f"[DISPATCHER] Sono nel metodo get.")
        CommandID = self.queue.get()

        return CommandID
