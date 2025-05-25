import Proto.StatisticsService_pb2 as IO_Parameters
import Proto.StatisticsService_pb2_grpc as Stub
import grpc,sys


if __name__ == "__main__":

    try:
        port = int(sys.argv[1])
    except:
        print("Errore: inserisci un porto valido.")
        exit(1)

    with grpc.insecure_channel(f"localhost:{port}") as channel:
        stub = Stub.StatisticsServiceStub(channel)
        
        sensors_iterable = stub.getSensors(IO_Parameters.Empty())


        for sensor in sensors_iterable:
            queried_sensor = IO_Parameters.MeanRequest(sensor_id=sensor.sensor_id,data_type=sensor.data_type)
            mean = stub.getMean(queried_sensor)
            print(f"[CLIENT] Media del sensore {sensor.sensor_id}: {mean.data}")
