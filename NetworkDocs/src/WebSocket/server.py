import hashlib
import socket
import base64
import struct
import random


def get_headers(data):
    # 获取请求头中的Websocket-Key
    header_dict = {}
    header_str = data.decode("utf8")
    for line in header_str.split("\r\n"):
        if line.startswith("Sec-WebSocket-Key"):
            header_dict["Sec-WebSocket-Key"] = line.split(":")[1].strip()
    return header_dict


def encode(msg):
    """消息加密"""
    byte = msg.encode("utf-8")
    token = b"\x81"
    length = len(byte)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)

    msg = token + byte

    return msg


def decode(data):
    """消息解密"""
    payload = data[1] & 127
    extend_payload_len = None
    mask = None
    decoded = None

    if payload == 127:
        extend_payload_len = data[2:10]  # 数据长度
        mask = data[10:14]  # 秘钥
        decoded = data[14:]

    elif payload == 126:
        extend_payload_len = data[2:4]  # 数据长度
        mask = data[4:8]  # 秘钥
        decoded = data[8:]

    elif payload <= 125:
        extend_payload_len = None  # 数据长度
        mask = data[2:6]  # 秘钥
        decoded = data[6:]

    # 开始解密
    str_byte = bytearray()
    for i in range(len(decoded)):
        byte = decoded[i] ^ mask[i % 4]
        str_byte.append(byte)

    return str_byte.decode("utf-8")


def websocket(tcp_client):
    # websocket加密秘钥
    websocket_string = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    data = tcp_client.recv(1024)  # 接受请求头

    value = get_headers(data).get("Sec-WebSocket-Key") + websocket_string
    # 对获取的数据结合websocket_string进行加密并编码
    ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())

    # 数据返回
    response_content = "HTTP/1.1 101 Switching Protocols\r\n" \
                       "Upgrade: websocket\r\n" \
                       "Connection: Upgrade\r\n" \
                       "Sec-WebSocket-Accept: {}\r\n" \
                       "Websocket-Location: ws://192.168.1.101:8888\r\n\r\n".format(ac.decode("utf-8"))

    tcp_client.send(response_content.encode("utf-8"))

    while True:
        try:
            data = tcp_client.recv(8096)
            if data:
                print(decode(data))
                tcp_client.send(encode("一边玩去~{}".format(random.randint(1, 10000))))
        except Exception as e:
            print(e.args)
            break
    tcp_client.close()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建socket链接
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 避免断开链接后阻塞
    sock.bind(("192.168.1.101", 8888))  # 绑定地址
    sock.listen(1024)  # 开始监听

    while True:
        tcp_client, address = sock.accept()  # 获取客户端sock

        try:
            websocket(tcp_client)
        except Exception as e:
            print(e.args)
            break

    sock.close()


if __name__ == '__main__':
    main()
