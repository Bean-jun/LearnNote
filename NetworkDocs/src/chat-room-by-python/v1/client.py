import socket
import threading

from common import *

class Boot:

    def __init__(self):
        self.socket_utils = SocketUtils()

    def Run(self):
        sock = self.socket_utils.create_server()
        sock.connect(("127.0.0.1", 7256))
        threading.Thread(target=self.get_sock_hander,
                         args=(sock, ), daemon=True).start()
        t = threading.Thread(target=self.set_sock_hander,
                             args=(sock, ))
        t.start()
        t.join()
        print("client exit")

    def get_sock_hander(self, sock: socket.socket):
        while True:
            msg = self.socket_utils.get_sock_msg(sock)
            if msg == "":
                continue
            print("recv from server msg: ", msg)

    def set_sock_hander(self, sock: socket.socket):
        while True:
            msg = input("请输入需要发送的消息: ")
            if msg == "":
                continue
            self.socket_utils.send_sock_msg(sock, msg)

            if msg == "bye":
                sock.close()
                break


if __name__ == "__main__":
    boot = Boot()
    boot.Run()
