1. TCP协议的三握四挥(来源于菜鸟教程)

   先看看图~ 

   **TCP报文首部格式**

![img](image/1538030297-3779-20150904110054856-961661137-20210905230123871.png)

   **TCP协议的三次握手和四次挥手**

![img](image/1538030297-7824-20150904110008388-1768388886.gif)



**三握四挥过程**

> **TCP连接建立过程：** 首先Client端发送连接请求报文，Server段接受连接后回复ACK报文，并为这次连接分配资源。Client端接收到ACK报文后也向Server段发生ACK报文，并分配资源，这样TCP连接就建立了。
>
> **TCP连接断开过程：** 假设Client端发起中断连接请求，也就是发送FIN报文。Server端接到FIN报文后，意思是说"我Client端没有数据要发给你了"，但是如果你还有数据没有发送完成，则不必急着关闭Socket，可以继续发送数据。所以你先发送ACK，"告诉Client端，你的请求我收到了，但是我还没准备好，请继续你等我的消息"。这个时候Client端就进入FIN_WAIT状态，继续等待Server端的FIN报文。当Server端确定数据已发送完成，则向Client端发送FIN报文，"告诉Client端，好了，我这边数据发完了，准备好关闭连接了"。Client端收到FIN报文后，"就知道可以关闭连接了，但是他还是不相信网络，怕Server端不知道要关闭，所以发送ACK后进入TIME_WAIT状态，如果Server端没有收到ACK则可以重传。"，Server端收到ACK后，"就知道可以断开连接了"。Client端等待了2MSL后依然没有收到回复，则证明Server端已正常关闭，那好，我Client端也可以关闭连接了。Ok，TCP连接就这样关闭了！

**为什么握手只要三次，挥手却要四次**

> **为什么要三次握手？**
>
> 在只有两次"握手"的情形下，假设Client想跟Server建立连接，但是却因为中途连接请求的数据报丢失了，故Client端不得不重新发送一遍；这个时候Server端仅收到一个连接请求，因此可以正常的建立连接。但是，有时候Client端重新发送请求不是因为数据报丢失了，而是有可能数据传输过程因为网络并发量很大在某结点被阻塞了，这种情形下Server端将先后收到2次请求，并持续等待两个Client请求向他发送数据...问题就在这里，Cient端实际上只有一次请求，而Server端却有2个响应，极端的情况可能由于Client端多次重新发送请求数据而导致Server端最后建立了N多个响应在等待，因而造成极大的资源浪费！所以，"三次握手"很有必要！
>
> **为什么要四次挥手？**
>
> 试想一下，假如现在你是客户端你想断开跟Server的所有连接该怎么做？第一步，你自己先停止向Server端发送数据，并等待Server的回复。但事情还没有完，虽然你自身不往Server发送数据了，但是因为你们之前已经建立好平等的连接了，所以此时他也有主动权向你发送数据；故Server端还得终止主动向你发送数据，并等待你的确认。其实，说白了就是保证双方的一个合约的完整执行！
>
> 使用TCP的协议：FTP（文件传输协议）、Telnet（远程登录协议）、SMTP（简单邮件传输协议）、POP3（和SMTP相对，用于接收邮件）、HTTP协议等。
>



2. 源码实现

   别害怕，我边写边加注释~

   ```python
   # NetworkDocs/TCP/server.py
   # 服务端
   
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
   ```

   ```python
   # NetworkDocs/TCP/client.py
   # 客户端
   
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
   ```

3. 应用场景

   当对网络通讯质量有要求的时候，比如：整个数据要准确无误的传递给对方，这往往用于一些要求可靠的应用，比如HTTP、HTTPS、FTP等传输文件的协议，POP、SMTP等邮件传输的协议。

