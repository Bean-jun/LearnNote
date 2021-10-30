## 授权系统

源码地址：`WebFrameDocs/src/demo`  下  `AuthSystem`

### 一、介绍

本项目将会制作一个授权系统，其他application程序均可以使用本授权系统实现注册、登录认证以及第三方授权...

### 二、简易流程

![image-20211004141731330](AuthSystem/docs/image/image-20211004141731330.png)

### 三、系统架构

暂时不确定，这里预计出两个版本，分别如下：

1. 版本一 授权、鉴权统一在AuthSystem服务器上

   ![image-20211004143948225](AuthSystem/docs/image/image-20211004143948225.png)

~~2. 版本二 授权鉴权分离，授权在AuthSystem服务器上，鉴权在AuthSystem客户机上~~

### 四、版本迭代计划

确定后期开发过程中实现的重点目标，以此实现产品快速开发，暂定Python实现，后期考虑使用golang重构

tag: 0.1 Oauth授权

~~1. 产品基本功能version 0.1 alpha~~

    - version 0.0.1使用django快速实现register
    - version 0.0.2使用django快速实现login
    - version 0.0.3 使用django快速实现第三方授权（微博[暂定]，....）

~~2. 产品开放授权鉴权version 0.2 alpha~~

    - version 0.1.1 使用jwt实现授权
    - version 0.1.2 使用jwt实现鉴权

~~3. 开放适用版本version 0.3 beta~~

    - 修复bug，推出适用版本

~~4. 性能优化 version 0.4 beta~~

~~5. 正式开放 version 0.5~~

    - 授权、鉴权统一
    - 授权鉴权分离

6. ....

### 五、API文档

点击查看[API文档](AuthSystem/docs/api文档.md)
