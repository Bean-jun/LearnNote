1. 基本的源码实现 ~ 

   别害怕，我边写边加注释~

   ```python
   # NetworkDocs/UDP/send.py
   # 发送方
   
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
   ```

   ```python
   # NetworkDocs/UDP/recv.py
   # 接收方
   
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
   ```

2. 应用场景

   当对网络通讯质量要求不高的时候，要求网络通讯速度能尽量的快的时候。

   小彩蛋：在好几年前有一款移植手游-`极品飞车(最高通缉)`就是基于UDP来实现通信的，有兴趣的小伙伴可以研究下~