from InterfacciaMagazzino import InterfacciaMagazzino
from multiprocessing import Queue


class MagazzinoImplementation(InterfacciaMagazzino):
    
    def __init__(self):
        self.CodaLaptop = Queue(3)
        self.CodaSmartphone = Queue(3)
    
    def deposita(self, articolo:str, id):
        # Struttura del pacchetto:
        # 
        # <deposita> # <nome_articolo> # <id>
        # 
        # NOTA: Nome articolo può essere solo Laptop o Smartphone
        # NOTA2: Si potrebbe implementare usando una coda di classi
        # per essere più precisi, ma vabbè
        #
        CodaSelezionata = None
        
        if articolo.strip() == "Laptop":
            CodaSelezionata = self.CodaLaptop
        elif articolo.strip() == "Smartphone":
            CodaSelezionata = self.CodaSmartphone
        else:
            print(f"[MAGAZZINO] Inserito articolo sconosciuto in deposita: {articolo}")
            return
            
        print(f"[MAGAZZINO] Inserito {articolo} nella coda.")
        CodaSelezionata.put(id)
    
    def preleva(self, articolo:str):
        CodaSelezionata = None
        
        if articolo.strip() == "Laptop":
            CodaSelezionata = self.CodaLaptop
        elif articolo.strip() == "Smartphone":
            CodaSelezionata = self.CodaSmartphone
        else:
            print(f"[MAGAZZINO] Inserito articolo sconosciuto in preleva: {articolo}")
            return
        
        print(f"[MAGAZZINO] Ritirato {articolo} dalla coda.")
        return CodaSelezionata.get()