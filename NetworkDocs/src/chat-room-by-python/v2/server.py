import socket
import threading

from common import *


class SocketRoom:

    def __init__(self):
        self.roomList = list()
        self.socket_utils = SocketUtils()

    def join_room(self, sock):
        self.roomList.append(sock)

    def exit_room(self, sock):
        if sock in self.roomList:
            self.roomList.remove(sock)

    def broasd_msg(self, sock, msg):
        for _sock in self.roomList:
            if _sock != sock:
                self.socket_utils.send_sock_msg(_sock, msg)


class Boot:

    def __init__(self):
        self.room = SocketRoom()
        self.socket_utils = SocketUtils()

    def Run(self):
        sock = self.socket_utils.create_server()
        sock.bind(("0.0.0.0", 7256))
        sock.listen(1)
        while True:
            _sock, addr = sock.accept()
            self.room.join_room(_sock)
            threading.Thread(target=self.sock_hander,
                             args=(_sock, addr)).start()

    def sock_hander(self, sock: socket.socket, addr):
        while True:
            msg = self.socket_utils.get_sock_msg(sock)
            if msg == "":
                continue
            if msg == "bye":
                self.room.exit_room(sock)
                sock.close()
                break

            msg = f"{addr[0]}: {addr[1]} ->{msg}"
            print("recv client msg: ", msg)

            self.room.broasd_msg(sock, msg)


if __name__ == "__main__":
    boot = Boot()
    boot.Run()
