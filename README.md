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

   文章在PythonDocs目录下的Python基础语法部分，相关code见PythonDocs/src

   涉及到Python的基本语法内容及使用，仅仅部分内容，需要学习更详细的知识点请结合`菜鸟教程`学习

   👉	[基础语法](PythonDocs/Python-基础语法.md)👈



2. 高级点的内容

   文章在PythonDocs目录下的Python高级干货部分，相关code见PythonDocs/src

   主要涉及到Python的闭包、装饰器、上下文管理器、生成器、迭代器、迭代对象、线程、进程、协程部分的内容

   👉	[闭包&装饰器](PythonDocs/Python-闭包&装饰器.md)👈
   
   👉	[上下文](PythonDocs/Python-上下文.md)👈
   
   👉	[生成器&迭代器&迭代对象](PythonDocs/Python-生成器&迭代器&迭代对象.md)👈



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



### 五、Web框架

1. Django

   Django是一个可以使Web开发工作愉快并且高效的Web开发框架。 使用Django，能够以最小的代价构建和维护高质量的Web应用。

   👉	[入门使用](WebFrameDocs/Django-入门.md)👈



2. Flask



