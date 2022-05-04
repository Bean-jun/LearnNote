### 一、说明

先前写过相关文章，传送门👉	[基于Socket的WebSocket协议实现](./基于Socket的WebSocket协议实现.md)👈

此源码是学习socketserver库后改造版本

### 二、源码实现

```python
import base64
import hashlib
import struct
from socketserver import BaseRequestHandler, ThreadingTCPServer


class BaseWebSocketRequetHander(BaseRequestHandler):

    WEBSOCKET_STRING = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    def __init__(self, request, client_address, server):
        self.key = None
        super().__init__(request, client_address, server)

    def get_headers(self, data):
        # 获取请求头中的Websocket-Key
        header_dict = {}
        header_str = data.decode("utf8")
        for line in header_str.split("\r\n"):
            if line.startswith("Sec-WebSocket-Key"):
                header_dict["Sec-WebSocket-Key"] = line.split(":")[1].strip()
        return header_dict

    def upgrade_websocket(self):
        """
        将链接改为websocket连接
        """
        if self.key is None:
            raise Exception("Sec-WebSocket-Accept is not null.")

        response_content = "HTTP/1.1 101 Switching Protocols\r\n" \
            "Upgrade: websocket\r\n" \
            "Connection: Upgrade\r\n" \
            "Sec-WebSocket-Accept: {key}\r\n" \
            "Websocket-Location: ws://{host}:{port}\r\n\r\n".\
            format(**{
                "key": self.key.decode("utf-8"),
                "host": self.server.server_address[0],
                "port": self.server.server_address[-1],
            })

        self.request.send(response_content.encode("utf-8"))

    def setup(self):
        """
        处理websocket

        GET / HTTP/1.1\r\n
        Host: 127.0.0.1:8888\r\n
        Connection: Upgrade\r\n
        Pragma: no-cache\r\n
        Cache-Control: no-cache\r\n
        User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36 Edg/90.0.818.56\r\n
        Upgrade: websocket\r\n
        Origin: http://localhost:63342\r\n
        Sec-WebSocket-Version: 13\r\n
        Accept-Encoding: gzip, deflate, br\r\n
        Accept-Language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6\r\n
        Sec-WebSocket-Key: 7iezRLm8rSVYShdK/uYauQ==\r\n
        Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits\r\n\r\n
        """
        # 获取请求头
        data = self.request.recv(1024)
        # 处理请求头
        value = self.get_headers(data).get(
            "Sec-WebSocket-Key") + BaseWebSocketRequetHander.WEBSOCKET_STRING
        self.key = base64.b64encode(
            hashlib.sha1(value.encode('utf-8')).digest())
        # 将链接升级为websocket
        self.upgrade_websocket()

    def websocket_decode(self, data):
        """
        数据解密
        :param data: 获取的字节流数据
        :return: 解析的结果
        """
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

    def websocket_encode(self, data):
        """
        数据加密
        :param msg: 需要加密数据
        :return: 加密后数据
        """
        byte = data.encode("utf-8")
        token = b"\x81"
        length = len(byte)
        if length < 126:
            token += struct.pack("B", length)
        elif length <= 0xFFFF:
            token += struct.pack("!BH", 126, length)
        else:
            token += struct.pack("!BQ", 127, length)
        data = token + byte
        return data

    def handle(self):
        raise Exception("please overridden")


class DemoWebSocketRequetHander(BaseWebSocketRequetHander):
    def handle(self):
        while True:
            try:
                data = self.request.recv(8096)
                if data:
                    print(self.websocket_decode(data))
                    import random
                    self.request.send(self.websocket_encode(
                        "hello~{}".format(random.randint(1, 10000))))
            except Exception as e:
                print(e.args)
            except KeyboardInterrupt as e:
                self.request.close()


def main(server_address, RequestHandlerClass):
    with ThreadingTCPServer(server_address, RequestHandlerClass) as sock:
        sock.serve_forever()


if __name__ == "__main__":
    main(("localhost", 8881), DemoWebSocketRequetHander)
```