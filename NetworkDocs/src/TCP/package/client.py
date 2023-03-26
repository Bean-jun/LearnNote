import socket
from common import *



# tcp
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.connect(("192.168.2.100", 9999))

while True:
    user_send_msg(sk)
    get_msg(sk)
