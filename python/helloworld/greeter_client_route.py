from __future__ import print_function
import logging

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.

    host = 'localhost'
    port = 1449
    with open(r'/home/wotaker/server.crt', 'rb') as f: # path to you cert location
        trusted_certs = f.read()

    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    #channel = grpc.secure_channel(‘{}:{}’.format(host, port), credentials)

    with grpc.secure_channel(f'{host}:{port}', credentials) as channel:
        stub1 = helloworld_pb2_grpc.GreeterV1Stub(channel)
        response1 = stub1.SayHello1(helloworld_pb2.HelloRequest(name='wotaker I'))
        print("Greeter client received: " + response1.message)

    with grpc.secure_channel(f'{host}:{port}', credentials) as channel:
        stub2 = helloworld_pb2_grpc.GreeterV2Stub(channel)
        response2 = stub2.SayHello2(helloworld_pb2.HelloRequest(name='wotaker II'))
        print("Greeter client received: " + response2.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
