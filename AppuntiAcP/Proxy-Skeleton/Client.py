import Proxy, random
from threading import Thread
from time import sleep

IP = 'localhost'
PORT = 5000

def thr_SendCommand(id):
    Client = Proxy.Proxy(ip=IP, port=PORT)
    
    for i in range(3):
        cmd = random.randint(0,3)
        print(f"[CLIENT] Thread {id}, mando {cmd} al server.")
        Client.sendCmd(cmd)
        sleep(random.randint(2,4))

if __name__ == "__main__":
    thr_list = []

    for i in range(5):
        t = Thread(target=thr_SendCommand,args=(i,))
        t.start()

        thr_list.append(t)

    for i in range(5):
        thr_list[i].join()