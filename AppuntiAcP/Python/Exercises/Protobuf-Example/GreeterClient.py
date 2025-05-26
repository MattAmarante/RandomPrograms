###################################################################
# NOTA: il codice non parte cosi com'è, ma deve essere modificato #
# rendendo ogni funzione unica, con nome diverso, e associandola  #
# al server                                                       #
###################################################################


import grpc,helloworld_pb2_grpc,helloworld_pb2

def generate_request():
    names = ["a","b"]
    for names_to_send in names:
        yield helloworld_pb2.HelloRequest(names_to_send)



# Streaming lato server
def run():

    with grpc.insecure_channel("localhost:50051") as channel:
        
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        for response in stub.SayHello(helloworld_pb2.HelloRequest(name="you")):
            print(f"[CLIENT] SayHello invoked with name: you")



# Streaming lato client
def run():

    with grpc.insecure_channel("localhost:50051") as channel:
        
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(generate_request())



#Streaming bidirezionale
def run():

    with grpc.insecure_channel("localhost:50051") as channel:
        
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        for response in stub.SayHello(generate_request()):
            print(f"[CLIENT] Response received: {response.messaggio}")