import socket


class SocketUtils:

    def create_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return sock

    def send_sock_msg(self, sock, msg):
        sock.send(msg.encode("utf8"))

    def get_sock_msg(self, sock):
        datalen = 2
        data = b""
        while True:
            temp = sock.recv(datalen)
            data += temp
            if len(temp) < datalen:
                break
        return data.decode()
