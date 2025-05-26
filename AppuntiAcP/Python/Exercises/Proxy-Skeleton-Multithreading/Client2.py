from Proxy import Proxy
from random import randint
from time import sleep
from threading import Thread
import sys

NUM_RICHIESTE = 3
NUM_THREAD = 5
dictionary = {
    0: "Laptop",
    1: "Smartphone"
}

def thd_PrelevaArticolo(port):
    p = Proxy(port)
    
    for _ in range(NUM_RICHIESTE):
        sleep(randint(2,4))
        
        articolo = randint(0,1)
        
        id = p.preleva(dictionary[articolo])
        print(f"[CLIENT] Ho ritirato {dictionary[articolo]}, con ID:{id}")


if __name__ == "__main__":
    PortNum = sys.argv[1]
    thd_list = []
    
    for _ in range(NUM_THREAD):
        t = Thread(target=thd_PrelevaArticolo,args=(PortNum,))
        thd_list.append(t)
        
        t.start()
    
    for i in range(NUM_THREAD):
        thd_list[i].join()