import socket
from common import *

# tcp
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sk.bind(("192.168.2.100", 9999))
sk.listen()

while True:
    request, client_address = sk.accept()
    while True:
        try:
            get_msg(request)
            
            user_send_msg(request)
        except Exception as e:
            print(e.args)
            break
    request.close()