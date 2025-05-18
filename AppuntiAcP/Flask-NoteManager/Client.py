# Programma utilizzato per gestire un dizionario salvato tra un
# client e server.
# La struttura del dizionario è identica in entrambi i casi, ed è
# formata da una coppia (id,nota) dove id è un uuid e nota è un altro
# dizionario formato da una coppia (text,tag). Questo vuol dire che una
# coppia del dizionario avrà una forma tipo:
# 
# {
#   id: {
#       "text":testo
#       "tag":tag
#    }
# }


import requests,random

BASE_URL = 'http://localhost:5000'

POSSIBLE_TAGS = ["AcP","Controlli","IdS","AI"]
POSSIBLE_TEXT = ["Oggi sono molto distratto",
                "Questo è l'argomento di oggi..",
                "Non ho capito nulla oggi.."]

notes = {}


def generateRandomNote() -> dict:
    dic = {}

    dic["text"] = random.choice(POSSIBLE_TEXT)
    dic["tag"] = random.choice(POSSIBLE_TAGS)

    return dic


def printResponse(resp:requests.Response):
    print(f"Status: {resp.status_code}")
    print(f"Contenuto: {resp.text}")
    print(f"Headers: {resp.headers}")


def postNote(note) -> str:
    """ 
    Manda una richiesta di POST al server contenente
    la nota. Il server risponde con l'id assegnato.

    Ritorno: id assegnato
    """

    response = requests.post(BASE_URL+"/note",json=note)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"[POST] La richiesta post della nota: \n{note}")
        print("Non ha avuto successo.")
        printResponse(response)
        return
    
    json_response = response.json()

    return json_response["id"]


def getNote(id):
    """
    Manda al server una richiesta GET per ottenere la nota
    a partire da un ID. Il server può rispondere con la nota
    associata all'ID o un messaggio d'errore.

    Ritorno: nota mandata dal server, o un dizionario vuoto
    """

    response = requests.get(BASE_URL+f"/note/{id}")

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"[GET] La richiesta get (singola) con id: \n{id}")
        print("Non ha avuto successo.")
        printResponse(response)
        return

    json_response = response.json()

    if json_response["result"] == "Note not found":
        return {}
    
    return json_response["result"]


def getAllNotes() -> list[dict]:
    """
    Manda al server una richiesta GET per ottenere
    tutti i contenuti del suo dizionario.
    Il server risponde con una lista contenente tutte
    le coppie chiavi,valore all'interno del dizionario

    Ritorno: lista contenente le coppie
    """

    response = requests.get(BASE_URL+f"/notes")

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"[GET] La richiesta get (all)")
        print("Non ha avuto successo.")
        printResponse(response)
        return
    
    #RIVEDI
    return response.json()


def putNote(note,id):
    """
    Manda una richiesta di PUT per aggiornare una nota.
    Il server può rispondere o con la nota aggiornata
    oppure con un messaggio d'errore se la nota
    non è stata trovata.

    Ritorno: nulla
    """

    response = requests.put(BASE_URL+f"/note/{id}",json=note)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"[PUT] La richiesta PUT, per la nota: \n{note}")
        print("Non ha avuto successo.")
        printResponse(response)
        return

    json_response = response.json()

    if json_response["result"] == "fail":
        print(f"[PUT] La nota con id: {id} non esiste sul server.")
    else:
        print("[PUT] Aggiornamento avvenuto con successo!")


def deleteNote(id):
    """
    Manda una richiesta di DELETE per eliminare una nota
    dal lato server. Il server può rispondere con un
    messaggio di successo o errore.

    Ritorno: nulla 
    """

    response = requests.delete(BASE_URL+f"/note",json={"id":id})

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"[DELETE] La richiesta delete della nota con id: \n{id}")
        print("Non ha avuto successo.")
        printResponse(response)
        return
    
    json_response = response.json()

    if json_response["result"] == "deleted":
        print("[DELETE] La nota è stata eliminata correttamente")
    else:
        print(f"[DELETE] Nota con id: {id} non trovata")

def deleteAll():
    """
    Manda un messaggio di DELETE al server per
    eliminare TUTTE le note. Il server risponde
    sempre con un messaggio di successo.

    Ritorno: nulla
    """    

    response = requests.delete(BASE_URL+"/notes")

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"[DELETE] La richiesta delete (all)")
        print("Non ha avuto successo.")
        printResponse(response)
        return

    print("[DELETE] Note eliminate con successo!")


if __name__ == "__main__":

    # Faccio la POST di due note random..
    for _ in range(2):
        randomNote = generateRandomNote()
        id = postNote(randomNote)

        notes[id] = randomNote
        print(f"\n[CLIENT] Aggiunta nuova nota: \n{randomNote}\nid:{id}\n")

    # Scelgo una nota random, ne invio una get
    # e la salvo localmente
    keylist = list(notes.keys())
    randomID = random.choice(keylist)

    serverDic = getNote(randomID)
    print(f"\n[CLIENT] Nota ricevuta:\n{serverDic}\nid:{id}\n")

    notes[randomID] = serverDic

    # Ottengo tutte le note salvate sul server
    # e le salvo localmente
    noteList = getAllNotes()

    for note in noteList:
        id = note["id"]
        noteContent = note["note"]
        print(f"\n[CLIENT] Nota della lista:\n{noteContent}\nid:{id}\n")

        notes[id] = noteContent
    
    # Genero una nuova nota randomica e la aggiorno
    # sul server
    print(f"\n[CLIENT] Vecchia nota:\n{notes[randomID]}\nid:{randomID}\n")

    randomNote = generateRandomNote()
    randomID = random.choice(keylist)

    putNote(randomNote,randomID)
    notes[randomID] = randomNote
    print(f"\n[CLIENT] Nuova nota:\n{notes[randomID]}\nid:{randomID}\n")

    # Elimino una nota casuale
    randomID = random.choice(keylist)
    deleteNote(randomID)
    print(f"\n[CLIENT] Nota eliminata:\n{notes[randomID]}\nid:{randomID}\n")

    # Elimino tutto
    deleteAll()