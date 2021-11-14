# LearnGuide

本着记录的心态将此前及之后学习的内容进行统一整理，放在此处存档，方便后续回忆。



### 一、快速笔记

1. 常用工具

   > 工欲善其事必先利其器

   👉	[工具使用](ToolsDocs/工具集合.md)👈



2. 食用指南

   > 多练习, 反复练习, 多看看书



### 二、Python从入门到入土

1. 基础点的内容

   👉	[基础语法](PythonDocs/Python-基础语法.md)👈



2. 高级点的内容

   👉	[闭包&装饰器](PythonDocs/Python-闭包&装饰器.md)👈

   👉	[上下文](PythonDocs/Python-上下文.md)👈

   👉	[生成器&迭代器&迭代对象](PythonDocs/Python-生成器&迭代器&迭代对象.md)👈
   
   👉	[理解元类](PythonDocs/Python-理解元类.md)👈



### 三、 网络编程

1. UDP协议&&TCP协议

   UDP用户数据报协议，是面向无连接的通讯协议，UDP数据包括目的端口号和源端口号信息，由于通讯不需要连接，所以可以实现广播发送。UDP通讯时不需要接收方确认，属于不可靠的传输，可能会出现丢包现象。

   👉	[基于Socket的UDP协议实现](NetworkDocs/基于Socket的UDP协议实现.md)👈

   TCP传输控制协议，是面向连接的，提供可靠交付，有流量控制，拥塞控制，提供全双工通信，面向字节流（把应用层传下来的报文看成字节流，把字节流组织成大小不等的数据块），每一条 TCP 连接只能是点对点的（一对一）。

   👉	[基于Socket的TCP协议实现](NetworkDocs/基于Socket的TCP协议实现.md)👈



2. HTTP协议

   HTTP超文本传输协议，它是基于TCP协议的应用层传输协议，简单来说就是客户端和服务端进行数据传输的一种规则。

   👉	[基于Socket的HTTP协议实现](NetworkDocs/基于Socket的HTTP协议实现.md)👈

 

3. WebSocket协议

   WebSocket 是一种在单个 TCP 连接上进行全双工通讯的协议，允许服务端主动向客户端推送数据。

   👉	[基于Socket的WebSocket协议实现](NetworkDocs/基于Socket的WebSocket协议实现.md)👈



### 四、数据库

1. MySQL



2. Redis

   Redis（Remote Dictionary Server )，即远程字典服务，支持网络、可基于内存亦可持久化的日志型、Key-Value型数据库。
   
   👉	[入门使用](DatabaseDocs/Redis-入门.md)👈
   👉	[事务](DatabaseDocs/Redis-事务.md)👈
   
   
   
3. MongoDB



### 五、Web框架

   个人建议先学习Django和Flask后再学习其他框架.....

1. [Django](https://docs.djangoproject.com/)     [中文文档](https://docs.djangoproject.com/zh-hans/)           推荐指数 ⭐️⭐️⭐️⭐️⭐️

   Django是一个可以使Web开发工作愉快并且高效的Web开发框架。 使用Django，能够以最小的代价构建和维护高质量的Web应用。

   👉	[入门使用](WebFrameDocs/Django-入门.md)👈

   **Demo:**
   
   👉   [基于django实现的PersonBlog](WebFrameDocs/src/demo/PersonBlogSystem-demo.md)👈   【需要最新版请点击[这里](https://github.com/Bean-jun/PersonBlogSystem.git)】
  
   👉   [基于django实现的AuthSystem](WebFrameDocs/src/demo/AuthSystem-demo.md)👈   【需要最新版请点击[这里](https://github.com/Bean-jun/AuthSystem.git)】


2. [Flask](https://flask.palletsprojects.com/)    [中文文档](https://dormousehole.readthedocs.io/en/latest/)               推荐指数 ⭐️⭐️⭐️⭐️⭐️

   Flask是一个使用Python编写的轻量级 Web 应用框架。其WSGI工具箱采用 Werkzeug ，模板引擎则使用 Jinja2。

   👉	[入门使用](WebFrameDocs/Flask-入门.md)👈
   
   👉	[flask源码分析第一弹](WebFrameDocs/Flask-源码分析.md)👈

   **Demo:**
   
   👉	[基于flask实现的api-demo](WebFrameDocs/src/demo/flask-demo-api.md)👈
   
   

3. [fastapi](https://fastapi.tiangolo.com/zh/tutorial/)    官方中文             推荐指数 ⭐️⭐️⭐️⭐️

   FastAPI 是一个用于构建 API 的现代、快速（高性能）的 web 框架，使用 Python 3.6+ 并基于标准的 Python 类型提示。

   **Demo:**
   
   👉	[基于fastAPI实现的文件对象存储](WebFrameDocs/src/demo/fileStorage.md)👈 【当前版本为0.1版，需要最新版的请点[这里](https://github.com/Bean-jun/fileStorage)】

   

4. [tornado](https://www.tornadoweb.org/en/stable/)    [中文文档](https://www.osgeo.cn/tornado/)           推荐指数 ⭐️⭐️⭐️⭐️

   Tornado是一个python web框架和异步网络库，最初开发于 FriendFeed . 通过使用非阻塞网络I/O，Tornado可以扩展到数万个开放连接，使其非常适合 long polling， WebSockets以及其他需要与每个用户建立长期连接的应用程序。

   - 图书推荐 [introduction to tornado](http://shouce.jb51.net/tornado/)       **大家有机会还是支持正版书籍哦**

   

5. [aiohttp](https://docs.aiohttp.org/en/stable/)   [中文文档](https://www.bookstack.cn/books/aiohttp-chinese-documentation)               推荐指数 ⭐️⭐️⭐️

   Asynchronous HTTP Client/Server for [asyncio](https://docs.aiohttp.org/en/stable/glossary.html#term-asyncio) and Python.



### 六、常用工具

1. [celery](https://github.com/celery/celery)

   一款非常简单、灵活、可靠的分布式系统，可用于处理大量消息，并且提供了一整套操作此系统的一系列工具
   
   👉	[入门使用](OtherDocs/celery使用.md)👈
   
2. [siege](https://www.joedog.org/siege-home)

   一款简单方便的压测工具

### 七、遇见的BUG

