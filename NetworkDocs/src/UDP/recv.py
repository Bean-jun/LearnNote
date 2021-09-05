import socket


def main():
    # 创建套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定本地ip
    sock.bind(("192.168.1.101", 8080))

    while True:
        # 接收数据
        recv_data = sock.recvfrom(1024)
        recv_msg = recv_data[0].decode()
        recv_addr = recv_data[1]
        print("接收到的消息为：", recv_msg, "地址来源于：", recv_addr, sep='\n')


if __name__ == '__main__':
    main()
