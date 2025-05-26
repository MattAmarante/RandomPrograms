###################################################################
# NOTA: il codice non parte cosi com'è, ma deve essere modificato #
# rendendo ogni funzione unica, con nome diverso, e associandola  #
# al client                                                       #
###################################################################

import helloworld_pb2_grpc,helloworld_pb2

# Streaming lato server
class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self,request,context):
        for i in range(0,5):
            yield helloworld_pb2.HelloReply(messaggio=f"Hello, {request.messaggio}")



# Streaming lato client
class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self,request_iterator,context):
        
        names = []
        for request in request_iterator:
            names.append(request.name)
        
        return helloworld_pb2.HelloReply(messaggio="Hello, "+' '.join(names)+".")



# Streaming bidirezionale
class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self,request_iterator,context):
        
        for request in request_iterator:
            names.append(request.name)
            yield helloworld_pb2.HelloReply(messaggio=f"Hello, {request.name}.")