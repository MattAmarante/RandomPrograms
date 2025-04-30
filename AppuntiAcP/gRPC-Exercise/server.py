###############################################
# NOTE: Il codice è attualmente incompleto    #
###############################################

import proto.OrderManagement_pb2
import proto.OrderManagement_pb2_grpc
import uuid

import grpc

class OrderManagementServicer(proto.OrderManagement_pb2_grpc.OrderManagementServicer):
    
    def __init__(self):
        self.orderDict = {}

    def getOrder(self, request, context):
        print("[SERVER] Received addOrder")
        id = uuid.uuid1()

        request.id = str(id)
        self.orderDict[request.id] = request

        response = proto.OrderManagement_pb2.StringMessage(value=str(id))
        print(self.orderDict)

        print(f"[SERVER] Order added with id: {id}")
        return response

    def getOrder(self, request, context):
        print(f"[SERVER] Received getOrder {request.value}")
        order = self.orderDict.get(request.value)
        
        if order is not None:
            print(f"[SERVER] Order {request.value} found")
            return order
        else:
            print(f"[SERVER] Order {request.value} not found")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Order: ", request.value, " Not Found")
            return proto.OrderManagement_pb2.Order()

    def searchOrders(self, request, context):
        print(f"[SERVER] Received searchOrder with {request.value}")
        matching_orders = self.searchInventory(request.value)

        print(f"[SERVER] Found {len(matching_orders)} orders")
        for order in matching_orders:
            yield order

    def processOrders(self, request_iterator, context):
        print(f"[SERVER] Received processOrders")

        location_dict = {}

        for order in request_iterator:

            if order.destination not in location_dict.keys():
                location_dict[order.destination] = [order]
            else:
                location_dict[order.destination].append(order)

        print(f"[SERVER] Generating {len(location_dict)} shipment/s")
        
        for key,values in location_dict.items():

            shipment_id = uuid.uuid1()
            shipment = proto.OrderManagement_pb2.CombinedShipment(id=shipment_id,
                                                                status="PROCESSED",
                                                                ordine=values)
            
            yield shipment


    def searchInventory(self, query):
        matching_orders = []

        for order_id, order in self.orderDict.items():
            for itm in order.items:

                if query in itm:
                    matching_orders.append(order)
                    break
        
        return matching_orders

