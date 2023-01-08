import grpc
from proto import hello_pb2, hello_pb2_grpc


if __name__ == "__main__":
    with grpc.insecure_channel("localhost:5000") as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(hello_pb2.HelloRequest(name="tom"))
        print(response.message)
