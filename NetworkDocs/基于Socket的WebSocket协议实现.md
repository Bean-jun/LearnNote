### 一、概念知识

1. 为何诞生

   WebSocket 是一种在单个 TCP 连接上进行全双工通讯的协议，允许服务端主动向客户端推送数据。

   直白点说就是：HTTP协议是我们常用的协议之一，但是它有个大问题：`HTTP是无连接`，那就意味着服务器处理完客户的请求，并收到客户的应答后，即**断开连接**，可是我现在就是不想断开哎！喂~ 不要这么高冷的断掉啊~ 刚好WebSocket协议刚好解决了这个问题。

   问：前端使用无限循环（轮询）不行嘛？

   答：可以，除非你呢对于TCP的三握四挥时间不在意；对于没有消息也占用服务器资源也不在意；hhhh :)

2. 原理知识

   它需要**借用**HTTP的协议来完成一部分握手，之后就可以建立客户端和服务端的链接了，这时就没HTTP什么事情了。简而言之：一次握手，长久使用

   ```shell
   # 客户端请求
   GET / HTTP/1.1
   Upgrade: websocket
   Connection: Upgrade
   Host: 192.168.1.101:8888
   Origin: http://192.168.1.101:8000
   Sec-WebSocket-Key: hBxp5WcU+GvqHiOWpKipIQ==
   Sec-WebSocket-Version: 13
   
   # 服务端响应
   HTTP/1.1 101 Switching Protocols
   Upgrade: websocket
   Connection: Upgrade
   Sec-WebSocket-Accept: n3NQ1Vd3cokG551zg4FLlsPkUmU=
   Sec-WebSocket-Location: ws://192.168.1.101:8888
   ```

3. 魔法字符串

   WebSocket目前你要使用到的一个特殊字符串`258EAFA5-E914-47DA-95CA-C5AB0DC85B11`

   服务器需要将客户端传输过来的`Sec-WebSocket-Key`使用这个魔法字符串通过`sha-1`及`base64`加密后传输给客户端来实现基本的认证操作，从而建立链接。

   

### 二、源码实现-demo

0. `socketserver` 实现版本 传送门 👉	[结合SocketServer库的WebSocket协议实现](./结合SocketServer库的WebSocket协议实现.md)👈

1. server版本

   ```python
   # NetworkDocs/WebSocket/server.py
   
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
   ```

2. 前端测试代码

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Websocket测试页面</title>
   </head>
   <body>
   <h1>websocket测试页面</h1>
   </body>
   <script type="application/javascript">
       $(function () {
           <!--创建ws对象-->
           var ws = new WebSocket("ws://192.168.1.101:8888")
   
           function send_msg(data) {
               setInterval(function () {
                   ws.send(data)
               }, 1000)
           }
   
           send_msg("dfgs")
       })
   
   </script>
   </html>
   ```

   

