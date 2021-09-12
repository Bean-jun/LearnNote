### 一、概念知识

1. HTTP的工作原理

   HTTP协议定义了Web客户端如何从Web服务器请求Web页面，以及服务器如何把Web页面传送给客户端。
   >
   > HTTP协议采用了请求/响应模型。
   >
   > 客户端向服务器发送一个请求报文，请求报文包含请求的方法、URL、协议版本、请求头部和请求数据。
   >
   > 服务器以一个状态行作为响应，响应的内容包括协议的版本、成功或者错误代码、服务器信息、响应头部和响应数据。

2. 关于HTTP的注意点

   > HTTP是无连接：无连接的含义是限制每次连接只处理一个请求。服务器处理完客户的请求，并收到客户的应答后，即**断开连接**。采用这种方式可以节省传输时间。
   > 
   > HTTP是媒体独立的：这意味着，只要客户端和服务器知道如何处理的数据内容，任何类型的数据都可以通过HTTP发送。客户端以及服务器指定使用适合的MIME-type内容类型。
   > 
   >HTTP是无状态：HTTP协议是无状态协议。无状态是指协议对于事务处理没有记忆能力。缺少状态意味着如果后续处理需要前面的信息，则它必须重传，这样可能导致每次连接传送的数据量增大。另一方面，在服务器不需要先前信息时它的应答就较快。

3. HTTP的请求消息格式

- 请求格式

![2012072810301161](image/2012072810301161.png)


百度网站的栗子-请求头

![image-20210912111134961](image/image-20210912111134961.png)

- 响应格式

![867021-20180322001744323-654009411](image/867021-20180322001744323-654009411.jpg)

百度网站的栗子-响应头

![image-20210912111153729](image/image-20210912111153729.png)

4. 常见的请求方式

   | 1    | GET     | 请求指定的页面信息，并返回实体主体。                         |
   | ---- | ------- | ------------------------------------------------------------ |
   | 2    | HEAD    | 类似于 GET 请求，只不过返回的响应中没有具体的内容，用于获取报头 |
   | 3    | POST    | 向指定资源提交数据进行处理请求（例如提交表单或者上传文件）。数据被包含在请求体中。POST 请求可能会导致新的资源的建立和/或已有资源的修改。 |
   | 4    | PUT     | 从客户端向服务器传送的数据取代指定的文档的内容。             |
   | 5    | DELETE  | 请求服务器删除指定的页面。                                   |
   | 6    | CONNECT | HTTP/1.1 协议中预留给能够将连接改为管道方式的代理服务器。    |
   | 7    | OPTIONS | 允许客户端查看服务器的性能。                                 |
   | 8    | TRACE   | 回显服务器收到的请求，主要用于测试或诊断。                   |
   | 9    | PATCH   | 是对 PUT 方法的补充，用来对已知资源进行局部更新 。           |



### 二、源码实现-demo

1. 创建server端--超级简易版

   ```python
   # NetworkDocs/HTTP/server.py
   
   import re
   import socket
   
   
   def send_2_client(tcp_client):
       # 向客户端发送数据
       recv = tcp_client.recv(1024).decode()
       recv = recv.splitlines()  # ['GET / HTTP/1.1', 'Host: 192.168.1.101:8080', 'Connection: keep-alive', ...]
   
       # 获取请求内容
       if recv:
           methods = None
           ret = None
           try:
               methods = re.match("^(.+?)\s", str(recv[0]))
               methods = methods.group(0).strip()
               ret = re.match("[^/]+(/[^ ]*)", str(recv[0]))
               ret = ret.group(1).strip()
           except Exception as e:
               print(e.args)
   
           if ret:
               headers = "HTTP/1.1 200 OK\r\n"
               headers += "content-type: text/html;charset=utf-8\r\n\r\n"
               import datetime
               headers += str("请求方式:{}, 响应结果：{}".format(methods, datetime.datetime.now()))
               tcp_client.send(headers.encode("utf-8"))
   
           print("{}-请求响应完毕....".format(tcp_client))
       else:
           tcp_client.close()
   
   
   def main():
       # 创建套接字
       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   
       # 绑定本地ip
       sock.bind(("192.168.1.101", 8080))
   
       # 开启监听
       sock.listen(128)
   
       while True:
           # 处理客户端连接
           response_client, response_address = sock.accept()
   
           try:
               send_2_client(response_client)
           except Exception as e:
               print(e.args)
               break
   
       # 关闭套接字
       sock.close()
   
   
   if __name__ == '__main__':
       main()
   ```

   小结：

   ​       仔细观察我们会发现，这个版本的server服务器在实现时，完成遵守了HTTP协议的请求协议-获取请求头-处理响应

   

2. 基于HTTP协议的简易文件下载服务器

   ```python
   # NetworkDocs/HTTP/file_server.py
   
   
   import re
   import socket
   
   
   def send_2_client(tcp_client):
       # 向客户端发送数据
       recv = tcp_client.recv(1024).decode()
       recv = recv.splitlines()  # ['GET / HTTP/1.1', 'Host: 192.168.1.101:8080', 'Connection: keep-alive', ...]
   
       # 获取请求内容
       if recv:
           methods = None
           ret = None
           try:
               methods = re.match("^(.+?)\s", str(recv[0]))
               methods = methods.group(0).strip()
               ret = re.match("[^/]+(/[^ ]*)", str(recv[0]))
               ret = ret.group(1).strip()
           except Exception as e:
               print(e.args)
   
           if ret:
               print("当前文件目录", ret)
               headers = "HTTP/1.1 200 OK\r\n"
   
               try:
                   with open("TestFile" + ret, 'r', encoding='utf-8') as f:
                       content = f.read()
               except Exception as e:
                   print(e.args)
                   content = ""
   
               if content:
                   headers += "Content-Disposition: attachment;filename={}\r\n\r\n".format(ret.strip("/"))
                   headers += content
               else:
                   headers += "content-type: text/html;charset=utf-8\r\n\r\n"
                   headers += "文件不存在"
   
               tcp_client.send(headers.encode("utf-8"))
   
           print("{}-请求响应完毕....".format(tcp_client))
   
       tcp_client.close()
   
   
   def main():
       # 创建套接字
       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   
       # 绑定本地ip
       sock.bind(("192.168.1.101", 8080))
   
       # 开启监听
       sock.listen(128)
   
       while True:
           # 处理客户端连接
           response_client, response_address = sock.accept()
   
           try:
               send_2_client(response_client)
           except Exception as e:
               print(e.args)
               break
   
       # 关闭套接字
       sock.close()
   
   
   if __name__ == '__main__':
       main()
   ```



3. 高性能版本

   都在用Python开发了，还要啥自行车啊，上面的用着吧!（ps：开个玩笑哈，后面补充完Python高级部分进程、线程、协程后更新该版本~ ）
