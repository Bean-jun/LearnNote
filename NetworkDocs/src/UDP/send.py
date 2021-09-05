import socket


def main():
    # 创建套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 发送数据
    while True:
        msg = input("请输入你想要发送的内容(`exit`退出)：\n")
        if msg == "exit":
            break
        sock.sendto(msg.encode('utf-8'), ("192.168.1.101", 8080))

    # 关闭套接字
    sock.close()


if __name__ == '__main__':
    main()
