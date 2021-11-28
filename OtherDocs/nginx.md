### 一. 基本概念

1. 正向代理

   简单理解为客户端需要通过代理服务器连接到资源服务器的过程，服务端对客户端的感知是未知的。这里服务端是暴露的，客户端被代理服务器隐藏了。

2. 反向代理

   简单理解为客户端访问代理服务器代理的多个服务器资源，客户端对服务端的感知是未知的。这里客户端是暴露的，服务端被代理服务器隐藏了。

3. 负载均衡

   将请求分发到多个服务器上，将负载分发到不同的服务器实现负载均衡。

   ```shell
   upstream servername {
   		# ip_hash # 将每个ip的hash进行分配，解决session共享问题
   		# weight # 权重，被分配的权重
   		ip_hash;
   		server 127.0.0.1:8000 weight=1;
   		server 127.0.0.1:8001 weight=1;
   		server 127.0.0.1:8002 weight=1;
   		server 127.0.0.1:8003 weight=1;
   }
   
   server {
   		listen 80;
   		server_name localhost;
   		
   		location / {
   				proxy_pass http://servername;		
   		}
   }
   ```

   例子

   ```shell
   http {
       upstream flaskapp {
           ip_hash;
           server 192.168.1.104:8080 weight=1;
           server 192.168.1.106:8080 weight=1;
           server 192.168.1.107:8080 weight=1;
           server 192.168.1.108:8080 weight=1;
       }
   
       server {
           listen 81;
           server_name localhost;
   
           location / {
               proxy_pass http://flaskapp;
           }
   
           location /static {
               alias /home/bean/PersonBlogUpdate/xxx;
           }
       }
   }
   ```




### 二、...

