from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)

def getDB():
    client = MongoClient("mongodb://localhost:27017/")
    return client['sensor-exercise']

@app.post("/sensor")
def addSensor():
    sensorData = request.get_json()

    try:
        id = sensorData["_id"]
        dataType = sensorData["data_type"]
    except KeyError:
        return {"result":f"Fail: formato sbagliato.\n {sensorData}"},400
    

    try:
        db = getDB()
        sensorCollection = db['sensors']
        sensorCollection.insert_one(sensorData)
    except:
        return {"result":"Fail: errore nel DB"},500
    else:
        return {"result":"success"}
    
@app.post("/data/<data_type>")
def addData(data_type):
    sentData = request.get_json()

    try:
        id = sentData["sensor_id"]
        dataType = sentData["data"]
    except KeyError:
        return {"result":f"Fail: formato sbagliato.\n {sentData}"},400
    
    
    try:
        db = getDB()
        selectedCollection = None

        if data_type == "temp":
            selectedCollection = db['temp-data']
        elif data_type == "press":
            selectedCollection = db['press-data']
        else:
            return {"result":f"Fail: non esiste una collezione collegata a {data_type}"}
        
        selectedCollection.insert_one(sentData)
    except:
        return {"result":"Fail: errore nel DB"},500
    else:
        return {"result":"success"}
    

if __name__ == "__main__":
    app.run()