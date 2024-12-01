import os

from concurrent import futures

import grpc

from idl.users_pb2 import ResponseLogin
from idl.users_pb2_grpc import UserServiceServicer, add_UserServiceServicer_to_server


class UserService(UserServiceServicer):
    def Login(self, request, context):
        print("Login")
        print(request.username)
        print(request.password)
        return ResponseLogin(valid=True, msg="登录成功")


def _load_credential_from_file(filepath):
    real_path = os.path.join(os.path.dirname(__file__), filepath)
    with open(real_path, "rb") as f:
        return f.read()


if __name__ == '__main__':
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_UserServiceServicer_to_server(UserService(), server)
    server.add_secure_port('[::]:50051', grpc.ssl_server_credentials(
        [(_load_credential_from_file("credentials/server.key"),
         _load_credential_from_file("credentials/server.pem"))]
    ))
    # server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()