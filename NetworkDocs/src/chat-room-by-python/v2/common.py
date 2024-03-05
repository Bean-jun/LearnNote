import struct
import socket


HeaderLength = 12
__format = "!3I"

def to_bytes(msg):
    if isinstance(msg, bytes):
        return msg
    if isinstance(msg, str):
        return msg.encode("utf-8")
    return str(msg).encode("utf-8")


def package(msg, version=1, cmd=100):
    __body = to_bytes(msg)
    __header = [version, len(__body), cmd]
    header = struct.pack(__format, *__header)
    body = header + __body
    return body


def unpackage(stroage, msg):
    if len(stroage) < HeaderLength:
        return

    __header = stroage[:HeaderLength]
    version, body_len, _ = struct.unpack(__format, __header)
    if len(stroage) < HeaderLength + body_len:
        return
    body = stroage[HeaderLength:HeaderLength+body_len]

    # 将当前存储数据进行释放，（粘包数据自动释放）
    stroage = stroage[HeaderLength+body_len:]

    return body


class SocketUtils:

    def create_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock

    def send_sock_msg(self, sock, msg):
        sock.send(package(msg))

    def get_sock_msg(self, sock):
        data = b""
        body = b""
        while True:
            msg = sock.recv(10)
            data += msg
            body = unpackage(data, msg)
            if body:
                break
        return body.decode()
