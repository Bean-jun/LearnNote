import socket


def main():
    # 创建套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 绑定本地ip
    sock.bind(("192.168.1.101", 8080))

    # 开启监听
    sock.listen(128)

    while True:
        # 处理客户端连接
        response_client, response_address = sock.accept()

        try:
            # 开始接收消息
            while True:
                try:
                    response_data = response_client.recv(1024)
                    if response_data:
                        print("当前地址为：", response_address, "获取到的消息为：", response_data.decode("utf-8"))
                    else:
                        break
                except Exception as e:
                    print(e.args)
                    break

            # 关闭客户端连接
            response_client.close()

        except Exception as e:
            print(e.args)
            break

    # 关闭套接字
    sock.close()


if __name__ == '__main__':
    main()
