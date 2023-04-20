# LearnGuide

本着记录的心态将此前及之后学习的内容进行统一整理，放在此处存档，方便后续回忆。



### 一、快速笔记

1. 常用工具

   > 工欲善其事必先利其器

   👉	[工具使用](ToolsDocs/工具集合.md)👈



2. 食用指南

   > 多练习, 反复练习, 多看看书



### 二、编程语言那些事

1. Python从入门到入土

   - 1.1 基础点的内容

      - 👉	[基础语法](PythonDocs/Python-基础语法.md)👈

   - 1.2 高级点的内容

      - 👉	[闭包&装饰器](PythonDocs/Python-闭包&装饰器.md)👈

      - 👉	[上下文](PythonDocs/Python-上下文.md)👈

      - 👉	[生成器&迭代器&迭代对象](PythonDocs/Python-生成器&迭代器&迭代对象.md)👈
      
      - 👉	[多线程](PythonDocs/Python-多线程.md)👈

      - 👉	[多进程](PythonDocs/Python-多进程.md)👈

      - 👉	[理解元类](PythonDocs/Python-理解元类.md)👈

      - 👉	[网络编程](#五网络编程)    (涉及TCP、UDP、HTTP协议)👈

      - 👉	[数据库编程](#六数据库)    (见数据库-ORM工具部分)👈
   
   - 1.3 无聊的代码

      - 👉	[重写os.walk工具](PythonDocs/Python-重写os.walk工具.md)👈

      - 👉	[限流-简单滑动窗口](PythonDocs/Python-简单滑动窗口.md)👈

   - 1.4 工作中常见

      - 👉	[常见代码](PythonDocs/Python-常见代码.md)👈

      - 👉	[Python-grpc&protobuf使用](PythonDocs/grpc&protobuf使用.md)👈
   
   - 1.5 无聊的轮子

      - 👉	[自定义Python Web Frame](https://github.com/Bean-jun/bframe) 【使用 `pip install bframe` 进行体验】👈

   - 1.6 Python相关文章推荐

      - 👉	[Python3多继承](https://www.python.org/download/releases/2.3/mro/) | [译文](https://lotabout.me/2020/C3-Algorithm/) | [见栗子-10](PythonDocs/Python-基础语法.md)👈
      - 👉	[【知乎】-Python部分魔法方法一览](https://zhuanlan.zhihu.com/p/344951719)👈
      - 👉	[【知乎】-Python包发布指南](https://zhuanlan.zhihu.com/p/115302375)👈
   
2. Golang从入门到入土

   - 2.1 基础点的内容

      - 👉	[基础语法](GolangDocs/Golang-基础语法.md)👈

      - 👉	[基础语法-操作MySQL](GolangDocs/Golang-操作MySQL.md)👈

      - 👉	[基础语法-RPC](GolangDocs/Golang-RPC.md)👈
   
   - 2.2 和grpc相关的内容

      - 👉	[Golang-grpc使用](GolangDocs/Golang-grpc使用.md)👈
   
   - 2.3 无聊的轮子

      - 👉	[自定义Golang Web Frame](GolangDocs/Golang-自定义Web框架.md) [| 视频介绍](https://www.bilibili.com/video/BV18D4y1k78d)👈

      - 👉	[手搓HTTP制作短链接生成器](GolangDocs/Golang-手搓HTTP制作短链接生成器.md) [| 视频介绍](https://www.bilibili.com/video/BV1Cs4y1H79U)👈

3. Java从入门到入土

   - 3.1 基础点的内容

      - 👉	[基础语法](JavaDocs/Java-基础语法.md)👈

      - 👉	[面向对象](JavaDocs/Java-面向对象.md)👈


4. 前端那些事【 仅学习笔记🙄 】

   - 4.1 前端基础

      - 👉	[HTML基础语法](FrontDocs/HTML-基础语法.md)👈

      - 👉	[CSS基础语法](FrontDocs/CSS-基础语法.md)👈

      - 👉	[JavaScript基础语法](FrontDocs/JavaScript-基础语法.md)👈
   
      - 👉	[JQuery基础语法](FrontDocs/JQuery-基础语法.md)👈
   
      - 👉	[Ajax基础语法](FrontDocs/Ajax-基础语法.md)👈

      - 👉	[Vue基础语法](FrontDocs/Vue-基础语法.md)👈



### 三、数据结构与算法

1. 不会点基础的说不过去咧

   👉	[基础数据结构&算法](https://github.com/Bean-jun/Base_Algorithm.git)👈

### 四、设计模式

1. 创建型模式

   👉	[设计模式-创建型模式](DesignDocs/设计模式.md#一创建型模式-介绍对象创建)👈



### 五、网络编程

1. UDP协议&&TCP协议

   UDP用户数据报协议，是面向无连接的通讯协议，UDP数据包括目的端口号和源端口号信息，由于通讯不需要连接，所以可以实现广播发送。UDP通讯时不需要接收方确认，属于不可靠的传输，可能会出现丢包现象。

   👉	[基于Socket的UDP协议实现](NetworkDocs/基于Socket的UDP协议实现.md)👈

   TCP传输控制协议，是面向连接的，提供可靠交付，有流量控制，拥塞控制，提供全双工通信，面向字节流（把应用层传下来的报文看成字节流，把字节流组织成大小不等的数据块），每一条 TCP 连接只能是点对点的（一对一）。

   👉	[基于Socket的TCP协议实现](NetworkDocs/基于Socket的TCP协议实现.md)👈

   👉	[基于Socket的简单封装对TCP粘包问题的小试牛刀](NetworkDocs/基于Socket的简单封装对TCP粘包问题的小试牛刀.md)👈



2. HTTP协议

   HTTP超文本传输协议，它是基于TCP协议的应用层传输协议，简单来说就是客户端和服务端进行数据传输的一种规则。[http协议参考](https://developer.mozilla.org/zh-CN/docs/Web/HTTP)

   👉	[基于Socket的HTTP协议实现](NetworkDocs/基于Socket的HTTP协议实现.md)👈

 

3. WebSocket协议

   WebSocket 是一种在单个 TCP 连接上进行全双工通讯的协议，允许服务端主动向客户端推送数据。

   👉	[基于Socket的WebSocket协议实现](NetworkDocs/基于Socket的WebSocket协议实现.md)👈

   👉	[结合SocketServer库的WebSocket协议实现](NetworkDocs/结合SocketServer库的WebSocket协议实现.md)👈
   
   
   - WebSocket实现库
     - [websockets](https://websockets.readthedocs.io)
     - [Channels](https://channels.readthedocs.io)




### 六、数据库

1. MySQL

   👉	[入门使用](DatabaseDocs/MySQL-入门.md)👈

2. Redis

   Redis（Remote Dictionary Server )，即远程字典服务，支持网络、可基于内存亦可持久化的日志型、Key-Value型数据库。
   
   👉	[入门使用](DatabaseDocs/Redis-入门.md)👈
   
   👉	[事务](DatabaseDocs/Redis-事务.md)👈
   
   👉	[持久化](DatabaseDocs/Redis-持久化.md)👈
   
   
   
3. MongoDB

4. ORM工具【非数据库】

   - [SQLAlchemy](https://www.sqlalchemy.org/)

      👉	[SQLAlchemy基本使用](OtherDocs/SQLAlchemy基本使用.md)👈

   - [peewee](http://docs.peewee-orm.com/en/latest/)


### 七、Web框架

1. [Django](https://docs.djangoproject.com/)     [中文文档](https://docs.djangoproject.com/zh-hans/)           推荐指数 ⭐️⭐️⭐️⭐️⭐️

   Django是一个可以使Web开发工作愉快并且高效的Web开发框架。 使用Django，能够以最小的代价构建和维护高质量的Web应用。

   推荐: [Django REST framework](https://www.django-rest-framework.org/)

   👉	[Django入门使用](WebFrameDocs/Django-入门.md)👈

   👉	[DRF入门使用](WebFrameDocs/DRF-入门.md)👈

   **Demo:**
   
   👉   [基于django实现的PersonBlog](https://github.com/Bean-jun/PersonBlogSystem.git)👈
  
   👉   [基于django实现的AuthSystem](https://github.com/Bean-jun/AuthSystem.git)👈
   
   


2. [Flask](https://flask.palletsprojects.com/)    [中文文档](https://dormousehole.readthedocs.io/en/latest/)               推荐指数 ⭐️⭐️⭐️⭐️⭐️

   Flask是一个使用Python编写的轻量级 Web 应用框架。其WSGI工具箱采用 Werkzeug ，模板引擎则使用 Jinja2。

   👉	[入门使用](WebFrameDocs/Flask-入门.md)👈

   👉	[flask-信号的使用](WebFrameDocs/Flask-信号的使用.md)👈
   
   👉	[flask源码分析第一弹](WebFrameDocs/Flask-源码分析.md)👈

   **Demo:**
   
   👉	[基于flask实现的api-demo](https://github.com/Bean-jun/PersonBlogSystemFlask/blob/master/docs/APIDocuments.md)👈
   
   

3. [fastapi](https://fastapi.tiangolo.com/zh/tutorial/)    官方中文             推荐指数 ⭐️⭐️⭐️⭐️

   FastAPI 是一个用于构建 API 的现代、快速（高性能）的 web 框架，使用 Python 3.6+ 并基于标准的 Python 类型提示。

   **Demo:**
   
   👉	[基于fastAPI实现的文件对象存储](https://github.com/Bean-jun/fileStorage)👈

   

4. [tornado](https://www.tornadoweb.org/en/stable/)    [中文文档](https://www.osgeo.cn/tornado/)           推荐指数 ⭐️⭐️⭐️⭐️

   Tornado是一个python web框架和异步网络库，最初开发于 FriendFeed . 通过使用非阻塞网络I/O，Tornado可以扩展到数万个开放连接，使其非常适合 long polling， WebSockets以及其他需要与每个用户建立长期连接的应用程序。

   - 图书推荐 [introduction to tornado](http://shouce.jb51.net/tornado/)       **大家有机会还是支持正版书籍哦**

   **Demo**

   👉	[一个基于rbac模型的crud架子](https://github.com/Bean-jun/tornado_demo.git)👈

   

5. [aiohttp](https://docs.aiohttp.org/en/stable/)   [中文文档](https://www.bookstack.cn/books/aiohttp-chinese-documentation)               推荐指数 ⭐️⭐️⭐️

   Asynchronous HTTP Client/Server for [asyncio](https://docs.aiohttp.org/en/stable/glossary.html#term-asyncio) and Python.



### 八、常用工具

1. [celery](https://github.com/celery/celery)

   一款非常简单、灵活、可靠的分布式系统，可用于处理大量消息，并且提供了一整套操作此系统的一系列工具
   
   👉	[入门使用](OtherDocs/celery使用.md)👈
   
2. [siege](https://www.joedog.org/siege-home)

   一款简单方便的压测工具

3. [nginx](https://nginx.org/)

   一款轻量级的Web服务器/反向代理服务器

   👉	[ubuntu下nginx简易安装](OtherDocs/nginx安装-Ubuntu.md)👈

   👉	[nginx中的一些基本概念](OtherDocs/nginx.md)👈

   👉 [nginx+uwsgi+django项目部署](DeployDocs/nginx_uwsgi_django部署.md)👈

   👉 [nginx+uwsgi+flask项目部署](DeployDocs/nginx_uwsgi_flask部署.md)👈
   
4. [uwsgi](https://uwsgi-docs-zh.readthedocs.io/zh_CN/latest/index.html)

   uWSGI是一个Web服务器，它实现了WSGI协议、uwsgi、http等协议

5. [docker](https://www.docker.com/)

    Docker 是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的镜像中，然后发布到任何流行的 Linux或Windows操作系统的机器上，也可以实现虚拟化。容器是完全使用沙箱机制，相互之间不会有任何接口。

   👉	[docker简易上手](OtherDocs/docker.md)👈

6. crontab

   特好用的定时执行程序的命令

   👉	[crontab操作文档(哈哈哈哈，我直接摘的操作手册)](OtherDocs/crontab.md)👈

7. [frp](https://gofrp.org/)

   内网穿透工具


### 九、开发知识

 1. cookies、session、token

    👉 [cookies、session、token到底是个啥?](DevelopDocs/cookie_session_token介绍.md)👈

 2. OAuth2、SSO

    👉 [OAuth2、SSO介绍](DevelopDocs/oauth2_sso介绍.md)👈

 3. LVS

    👉 [LVS介绍（转载）](DevelopDocs/LVS介绍.md)👈



### 十、遇见的BUG

 1. cookie离谱的生效范围

      👉 [cookie离谱的生效范围](BugDocs/cookies/cookie离谱的生效范围.md)👈

 2. go 加密库 slow bug

      👉 [go加密库执行慢的bug](BugDocs/go加密库执行慢的bug.md)👈

 3. 看似无害的工具-->解决文件名冲突的工具函数竟是程序变慢的元凶

      👉 [解决文件名冲突的工具函数竟是slow的元凶](BugDocs/解决文件名冲突的工具函数竟是slow的元凶.md)👈


### 十一、其他

 1. Jetson Nano B01 环境搭建 

      👉 [Jetson Nano环境搭建](TryDocs/Jetson_Nano_环境搭建.md)👈

 2. pyinstaller打包小技巧

      👉 [Pyinstaller工具小Tips](TryDocs/Pyinstaller工具小tips.md)👈
 
 3. py to pyd

      👉 [Py快速将py脚本编译为pyd](TryDocs/Py快速将py脚本编译为pyd.md)👈