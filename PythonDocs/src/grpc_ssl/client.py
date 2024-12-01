import os

import grpc
from idl.users_pb2 import RequestLogin
from idl.users_pb2_grpc import UserServiceStub


def _load_credential_from_file(filepath):
    real_path = os.path.join(os.path.dirname(__file__), filepath)
    with open(real_path, "rb") as f:
        return f.read()

if __name__ == '__main__':
    # with grpc.insecure_channel('localhost:50051') as channel:
    with grpc.secure_channel('localhost:50051', grpc.ssl_channel_credentials(
            _load_credential_from_file("credentials/server.pem")
    )) as channel:
        userService = UserServiceStub(channel)
        res = userService.Login(RequestLogin(username="test", password="<PASSWORD>"))
        print(res.msg, res.valid)
        print(res)