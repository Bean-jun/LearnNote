import socket


def main():
    # 创建套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接服务器
    sock.connect(("192.168.1.101", 8080))

    while True:
        msg = input("请输入你想要发送的内容(`exit`退出)：\n")
        if msg == "exit":
            break
        sock.send(msg.encode('utf-8'))

    # 关闭套接字
    sock.close()


if __name__ == '__main__':
    main()