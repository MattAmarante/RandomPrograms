import Proto.StatisticsService_pb2 as IO_Parameters
import Proto.StatisticsService_pb2_grpc as Stub
import grpc
from pymongo import MongoClient
from concurrent import futures

def getDB():
    client = MongoClient("mongodb://localhost:27017/")
    return client['sensor-exercise']

class MyServicer(Stub.StatisticsServiceServicer):
    
    def getMean(self, request, context):
        sensor_id = int(request.sensor_id)
        data_type = request.data_type

        try:
            db = getDB()
            
            if data_type == "temp":
                selectedCollection = db['temp-data']
            elif data_type == "press":
                selectedCollection = db['press-data']
            else:
                return IO_Parameters.StringMessage(data=f"Non esiste collezione per il data type {data_type}")
            
            sensorData = selectedCollection.find({'sensor_id':sensor_id})
        except:
            print("[SERVER] Errore nel DB.")
            return
        
        mean = 0
        total = 0
        n_measurement = 0

        for measurement in sensorData:
            try:
                queried_data = measurement['data']
                
                total = total + queried_data
                n_measurement = n_measurement + 1
            except KeyError:
                print(f"[SERVER] Dati del sensore sbagliati: \n{measurement}")
                continue
        
        if n_measurement != 0:
            mean = total/n_measurement
        else: 
            mean = 0
        
        return IO_Parameters.StringMessage(data=str(mean))
    
    def getSensors(self, request, context):
        try:
            db = getDB()
            sensorCollection = db['sensors']

            allSensors = sensorCollection.find()
        except:
            print("[SERVER] Errore nel DB.")
            return
        
        for sensor in allSensors:
            sensor_id = None
            data_type = None

            try:
                sensor_id = str(sensor['_id'])
                data_type = sensor['data_type']
            except KeyError:
                print(f"[SERVER] Dati del sensore sbagliati: \n{sensor}")
                continue

            yield IO_Parameters.Sensor(sensor_id=sensor_id,data_type=data_type)

if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Stub.add_StatisticsServiceServicer_to_server(MyServicer(),server)
    
    port = server.add_insecure_port("[::]:0")
    print(f"[SERVER] In ascolto su porto: {port}")

    server.start()

    server.wait_for_termination()
