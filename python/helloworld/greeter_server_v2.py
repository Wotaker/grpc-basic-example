from concurrent import futures
import time
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class GreeterV2(helloworld_pb2_grpc.GreeterV2Servicer):

    def SayHello2(self, request, context):
        return helloworld_pb2.HelloReply(message=f'Hello {request.name} from Greeter V2!')


def serve():
    port = '50052'

    with open(r'/home/wotaker/server.key', 'rb') as f: #path to you key location 
        private_key = f.read()
    with open(r'/home/wotaker/server.crt', 'rb') as f: #path to your cert location
        certificate_chain = f.read()
    server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterV2Servicer_to_server(GreeterV2(), server)
    server.add_secure_port('[::]:' + port, server_credentials)
    # server.add_insecure_port('[::]:50050')
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    logging.basicConfig()
    serve()
