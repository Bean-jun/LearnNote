# LearnGuide

本着记录的心态将此前及之后学习的内容进行统一整理，放在此处存档，方便后续回忆。



### 一、快速笔记

1. Python安装地址

   ```shell
   # 去官网download
   https://www.python.org
   # 在华为镜像站download
   https://repo.huaweicloud.com/python/
   ```

2. Python快速更换pip源

   ```shell
   # 更新源到清华大学开源镜像站点
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pip -U
   pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
   ```

3. Git下载

   ```shell
   # 官网
   https://git-scm.com
   # 华为源
   https://repo.huaweicloud.com/git-for-windows/
   https://repo.huaweicloud.com/git-for-macos/
   ```

4. vscode下载

   ```shell
   https://code.visualstudio.com
   ```



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
