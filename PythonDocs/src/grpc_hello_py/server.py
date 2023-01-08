from concurrent import futures

import grpc
from proto import hello_pb2, hello_pb2_grpc


class Greeter(hello_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return hello_pb2.HelloReply(message=f"你好，{request.name}")


if __name__ == "__main__":
    # 创建server
    server = grpc.server(futures.ThreadPoolExecutor(10))
    # 注册至server
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    # 启动server
    server.add_insecure_port("localhost:5000")
    server.start()
    server.wait_for_termination()
