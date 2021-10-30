### 一. 开始内容

- 0.1 git clone 项目

    ```shell
    git clone https://github.com/Bean-jun/PersonBlogSystem.git
    ```

- 0.2 配置文件

    ```shell
    0.2.1 django项目的settings配置
    
    这部分直接放在setup.py文件最佳，方便后期直接更新blog
        # 安全秘钥
        SECRET_KEY = 'xxx'
    
        # 调试模式及全站访问
        DEBUG = False
        ALLOWED_HOSTS = ['*']
    
        # 用于静态文件收集
        # python manage.py collectstatic
        STATIC_ROOT = 'xxx'
    
        # 管理员账号
        ADMIN_ACCOUNT = ['xxx']
    
        # 腾讯云对象存储
        TENCENT_SECRET_ID = 'xxx'
        TENCENT_SECRET_KEY = 'xxx'
    
        # 访客注册账号存储桶
        TENCENT_BUCKET = 'PersonBlog-visitor-1305490799'
        TENCENT_REGION = 'ap-shanghai'
    
        # 语雀账户Token - 供同步语雀平台数据使用
        YUQUE_TOKEN = "xxxxxxx"
        
        # 配置缓存
        CACHES = {
            "default": {
                "BACKEND": "django_redis.cache.RedisCache",
                "LOCATION": "redis://127.0.0.1:6379/1",
                "OPTIONS": {
                    "CLIENT_CLASS": "django_redis.client.DefaultClient",
                }
            }
        }
        
        # 配置session存储到缓存中
        SESSION_ENGINE = "django.contrib.sessions.backends.cache"
        SESSION_CACHE_ALIAS = "default"
    
    0.2.2 uwsgi.ini的配置
    
    这部分直接放在uwsgi.ini中即可,其中chdir，check-static，static-map和STATIC_ROOT保持一致即可
        [uwsgi]
        #使用nginx连接时使用
        socket=127.0.0.1:8080
        #项目目录
        chdir='xxx'
        #项目中wsgi.py文件的目录，相对于项目目录
        wsgi-file=PersonBlog/wsgi.py
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

- 0.3 nginx部分，百度下吧

### 2. 基本操作

- 1.1 关闭uwsgi

    ```shell
    uwsgi --stop uwsgi.pid
    ```

- 1.2 搜集静态文件

    ```shell
    python3 manage.py collectstatic
    ```

- 1.3 启动uwsgi

    ```shell
    uwsgi --ini uwsgi.ini
    ```

### 2. 更新小站

    重复第一大步的三个基本操作，不过需要在1，2之间来上一个git pull即可

### 3. 看看小站跑起来没

    有问题欢迎发issues

