### 一、安装uwsgi

```shell
pip install uwsgi
```



### 二、编辑uwsgi配置文件&&启动uwsgi

1. 编辑配置文件`uwsgi.ini`

- flask

   ```shell
   [uwsgi]
   socket = 127.0.0.1:8090
   chdir = "项目路径"
   pythonpath= "项目虚拟环境"
   wsgi-file = "项目启动文件"
   callable = "调用对象"
   processes=2
   threads=1
   master=True
   pidfile=uwsgi.pid
   daemonize=uwsgi.log
   ```

- django

   ```shell
   [uwsgi]
   #使用nginx连接时使用
   socket=127.0.0.1:8080
   #项目目录
   chdir='/var/PersonBlog'
   #项目中wsgi.py文件的目录，相对于项目目录
   wsgi-file='PersonBlog/wsgi.py'
   processes=2
   threads=1
   master=True
   pidfile=uwsgi.pid
   daemonize=uwsgi.log
   module = PersonBlog.wsgi:application
   # 用于检查静态文件目录
   check-static = 'xxx'
   # =前面的/static是uWSGI的URL前缀，而后面的/srv/django/static则是静态文件的路径。 这个路径，通常使用绝对路径，但也支持相对路径。
   static-map = 'xxx'
   ```

2. 启动uwsgi

   ```shell
   uwsgi --ini uwsgi.ini
   ```

   

### 三、编辑nginx配置文件

```shell
#user  nobody;
worker_processes  1;

events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    upstream yourservername {
        # ip_hash # 将每个ip的hash进行分配，解决session共享问题
        # weight # 权重，被分配的权重
        ip_hash;
        server 127.0.0.1:8090 weight=1;
        
        # 注意这里，建议多写uwsgi配置文件，分别启动，实现简单的负载均衡
        server 127.0.0.1:8001 weight=1;
        server 127.0.0.1:8002 weight=1;
        server 127.0.0.1:8003 weight=1;
    }

    server {
        listen       80;
        server_name  localhost;

        location / {
            include uwsgi_params;
            uwsgi_pss yourservername;
        }

        location /static {
        		# 静态文件所在路径
            alias /var/PersonBlog/xxx;
        }
    }
}
```



### 四、启动nginx

```shell
./nginx -s reload
```



### 五、查看结果

点开浏览器，查看结果...