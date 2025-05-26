import socket,random,Proxy
from time import sleep
from datetime import datetime

IP = 'localhost'
PORT = 5000

cmdString = {
    0: "Leggi",
    1: "Scrivi",
    2: "Configura",
    3: "Reset"
}

if __name__ == "__main__":
    Actuator = Proxy.Proxy(ip=IP, port=PORT)

    while True:
        
        sleep(1)

        cmd = Actuator.getCmd()
        print(f"[ACTUATOR] Ricevuto comando: {cmdString[cmd]}")

        with open("cmdlog.txt","a") as cmdlog:
            cmdlog.write(f"[{datetime.now()}] Comando ricevuto: {cmdString[cmd]:<10}\n")
