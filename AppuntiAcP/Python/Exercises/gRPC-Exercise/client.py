###############################################
# NOTE: Il codice è attualmente incompleto    #
###############################################

import proto.OrderManagement_pb2
import proto.OrderManagement_pb2_grpc
import uuid

import grpc


def run():

    # Definisci stub

    orders = []

    orders.append(proto.OrderManagement_pb2.Order(price=2450.24,
                                                    items=["mandorla","noce"],
                                                    description="Nocciolina",
                                                    destination="Napoli"))

    for order in orders:
        response = stub.addOrder(order)
        print(f"[CLIENT] Add order response: {response}")
        
        order = stub.getOrder(response)
        print(f"[CLIENT] Order service response {order}")
    
    for order_search_result in stub.searchOrder(proto.OrderManagement_pb2.StringMessage(value="mandorla")):
        print(f"[CLIENT] Search Result: {order_search_result}")
    