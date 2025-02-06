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



### 二、常见模块

1. auth_request 实现nginx端鉴权控制  官方介绍[https://nginx.org/en/docs/http/ngx_http_auth_request_module.html]#(`https://nginx.org/en/docs/http/ngx_http_auth_request_module.html`)

   auth_request指令允许放在http、server和location上下文中，在配置好后，每当指定的作用域在收到HTTP请求时，Nginx会向指定的路径发起一个GET类型的子请求，子请求的请求头部分与原HTTP请求的请求头部分一致。

   如果子请求收到2xx响应代码，则Nginx将允许原HTTP请求，如果子请求返回401或403响应代码时，则Nginx将使用相应的错误代码拒绝原HTTP请求，其他响应代码，则被视为错误。

   ```shell
   location /private/ {					# 请求想走/private/接口
       auth_request /auth;				# 走之前需要在此处进行/auth接口的权限校验
       ...												# 下面是/private/接口的具体路径
   }
   
   location = /auth {						# /auth授权
       proxy_pass ...						# 具体代理到那个授权接口 eg:http://127.0.0.1:5000/api/nginx/auth
       proxy_pass_request_body off;
       proxy_set_header Content-Length "";	# Content-Length请务必设置为""
       proxy_set_header X-Original-URI $request_uri;
   }
   ```

