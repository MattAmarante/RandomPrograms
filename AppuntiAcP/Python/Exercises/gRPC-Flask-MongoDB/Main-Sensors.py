import requests, random
from threading import Thread

NUM_SENSORS = 5
NUM_MISURAZIONI = 5
POSSIBLE_DATATYPE = ["temp","press"]
BASE_URL = "http://localhost:5000"

def thd_SensorFnc(sensor_id,data_type):
    
    # Registrazione presso il server
    sensorData = {"_id":sensor_id,"data_type":data_type}
    response = requests.post(url=BASE_URL+"/sensor", json=sensorData)

    json_response = response.json()

    if json_response["result"] != "success":
        print(f"[THREAD] Sensor {sensor_id} ha fallito la registrazione.")
        print(f"Messaggio ricevuto: \n{json_response["result"]}")
        return
    
    # Invio misurazioni
    for i in range(NUM_MISURAZIONI):
        misurazione = random.randint(0,50)
        measureData = {"sensor_id":sensor_id,"data":misurazione}

        measure_response = requests.post(url=BASE_URL+f"/data/{data_type}", json=measureData)
        json_measureResponse = measure_response.json()

        if json_measureResponse["result"] != "success":
            print(f"[THREAD] Sensor {sensor_id} ha fallito la misurazione.")
            print(f"Messaggio ricevuto: \n{json_measureResponse["result"]}")
            return
        else:
            print(f"[THREAD] Sensor {sensor_id} ha mandato la misurazione:")
            print(measureData)

if __name__ == "__main__":
    thd_list = []

    for i in range(NUM_SENSORS):
        selected_dataType = random.choice(POSSIBLE_DATATYPE)
        t = Thread(target=thd_SensorFnc,args=(i,selected_dataType))
        thd_list.append(t)

        t.start()

    for i in range(NUM_SENSORS):
        thd_list[i].join()