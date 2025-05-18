from flask import Flask,request
import random,uuid


app = Flask(__name__)
notes = {}


@app.post("/note")
def postNote():
    """
    Riceve una nota dal client e la aggiunge al dizionario
    generando un UUID da restituire.

    Ritorno: dizionario con messaggio di successo e ID
    """

    recv_note = request.get_json()
    id = str(uuid.uuid4())

    notes[id] = recv_note

    return {"result":"added","id":id}


@app.get("/note/<id>")
def getNote(id):
    """
    Riceve dal client l'id della nota da restituire.

    Ritorno: nota oppure messaggio d'errore
    """

    keylist = list(notes.keys())

    if id in keylist:
        return {"result":notes[id]}
    else:
        return {"result": "Note not found"}


@app.get("/notes")
def getAllNotes():
    """
    Ritorna una lista contenente tutte le note
    """
    noteList = []

    for id in notes:
        noteList.append({"note":notes[id],"id":id})

    return noteList


@app.put("/note/<id>")
def putNote(id):
    """
    Riceve una nota da assegnare ad un determinato ID

    Ritorno: dizionario con nuova nota o messaggio di errore
    """

    nota = request.get_json()
    keylist = list(notes.keys())

    if id in keylist:
        notes[id] = nota
        return {"result":nota,"id":id}
    else:
        return {"result":"Note not created","id":"-1"}


@app.delete("/note")
def deleteNote():
    """
    Riceve un id della nota da eliminare

    Ritorno: messaggio di successo o errore
    """
    
    id = request.get_json()["id"]
    keylist = list(notes.keys())

    if id in keylist:
        notes.pop(id)
        return {"result":"deleted","id":id}
    else:
        return {"result":"Note not found","id":"-1"}


@app.delete("/notes")
def deleteAll():
    """
    Elimina tutte le note dal dizionario
    """

    notes.clear()
    return {"result":"No more notes."}


if __name__ == "__main__":
    app.run(debug=True)