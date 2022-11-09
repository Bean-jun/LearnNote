### 1. 操作基础

#### 1. 1 安装

```shell
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

```shell
# 国内 daocloud 一键安装命令
curl -sSL https://get.daocloud.io/docker | sh
```

#### 1.2  卸载

```shell
# 删除安装包
sudo apt-get purge docker-ce
# 删除镜像、容器、配置文件等内容：
sudo rm -rf /var/lib/docker
```

#### 1.3  镜像加速

```shell
# 科大镜像：https://docker.mirrors.ustc.edu.cn/
# 网易：https://hub-mirror.c.163.com/
# 七牛云加速器：https://reg-mirror.qiniu.com

# 在 /etc/docker/daemon.json 中写入如下内容（如果文件不存在请新建该文件）：
{"registry-mirrors":["https://docker.mirrors.ustc.edu.cn/"]}

# 然后重启docker哦！
```

#### 1.4  测试安装

```shell
sudo docker run hello-world
```



### 2. 操作

#### 2.1 镜像基础命令

```shell
# 列出本地主机上镜像
docker images

# 查找网络上的镜像
docker search xxx

# 获取镜像
docker pull xxx

# 删除镜像
docker rmi xxx

# 提交最新镜像
docker commit -m="message" -a="author" 原镜像 新镜像
```

#### 2.2 容器使用

```shell
# 启动容器
docker run -it xxx

####
-i: 交互式操作。
-t: 终端。
-d: 后台运行。
-P:将容器内部使用的网络端口随机映射到我们使用的主机上。
####

# 停止容器
docker stop <容器ID>

# 重启容器
# 通过docker ps -a来获取容器ID
docker start <容器ID>

# 删除容器
docker rm <容器ID>
# 删除所有容器
docker rm -f $(docker ps -qa)

# 进入容器
docker attach -it <容器ID>	[/bin/bash]	# 不推荐
docker exec -it <容器ID> [/bin/bash] # 退出后不会导致容器停止

# 退出容器
exit

# 拷贝文件
docker cp 文件 <容器ID>:/目录 # 主机到容器
docker cp <容器ID>:/目录 文件	# 容器到主机

# 查看端口映射
docker port <容器ID>

# 查看容器的底层信息
docker inspect xxx
```



#### 2.3 容器的挂载

```shell
# 挂载容器
docker run -it -v 卷名:容器内路径

####
-v: 挂载地址
####

# 查看数据卷
docker volume ls

# docker 卷没有指定卷地址时默认地址
/var/lib/docker/volumes/

# 容器间数据共享
docker run -it -volumes-from 卷名 镜像
```



### 3. Dockfile

#### 3.1 介绍

```shell
FROM				# 基础镜像
LABEL				# 镜像作者
RUN					# docker 构建时需要运行的命令
ADD					# 添加内容压缩包
WORKDIR			# 工作目录
VOLUME			# 添加数据卷
EXPOSE			# 暴露端口
CMD					# 指定这个容器启动时需要运行的命令,只有最后一个会生效，可被替代
ENTRYPOINT	# 指定这个容器启动时需要运行的命令,可以追加命令
ONBUILD			# 当构建一个被继承Dockerfile 会被执行，触发执行
COPY				# 类似ADD,将文件导入到镜像中
ENV					# 构建时设置环境变量
```

#### 3.2构建image

```shell
docker build -f dockerfile文件 -t 构建镜像名:[tag]
```

#### 3.3 demo

通过dockerfile构建镜像

```shell
# 目录树
.
├── Dockerfile
├── app.py
├── requirements.txt
└── run.sh
```

```dockerfile
# Dockerfile

FROM    python:latest
LABEL   email="1342104001@qq.com"
ENV     home /root
WORKDIR ${home}
COPY    app.py ${home}
COPY    requirements.txt ${home}
RUN     python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE  5000
CMD     [ "python", "app.py"]
```



```python
# app.py

from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return {
        "code": 200,
        "message": "success",
        "data": {
            "name": "tom",
            "age": 12
        }
    }


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
```

```shell
# requirements.txt

Flask==2.0.2
```

```shell
# run.sh

# 存在即删除
docker rm -f fapp

# 启动镜像
docker run -itd -p 5001:5000 --name fapp application
```



### 4. 网络

```shell
# docker 启动容器时，默认使用birdge模式，这种模式会有一个问题：局域网内容器之间通信可能异常
# 解决方案： 创建网络，启动时指定网络即可

# 创建网络 子网：192.168.1.200/24  网关：192.168.1.200
docker network create --subnet 192.168.1.200/24 --gateway 192.168.1.200 localhost

# 以当前创建的网络进行启动  注意：--network localhost  表示以当前网络启动
docker run -td --name fapp1 --network localhost -p 5000:5000 镜像
```



### 5. docker-compose

#### 5.1 介绍

```shell
# 解决容器编排问题，通过yml文件一键启动docker镜像
# Compose 使用的三个步骤：
#		使用 Dockerfile 定义应用程序的环境。
#		使用 docker-compose.yml 定义构成应用程序的服务，这样它们可以在隔离环境中一起运行。
#		最后，执行 docker-compose up 命令来启动并运行整个应用程序。

# 启动命令
docker-compose up .
```

#### 5.2 编排命令

docker-compose的yml文件主要分为三个板块，通过这三个板块内容的编辑实现容器编排。分别为:

- 版本 `version`
- 服务 `services`
- 其他 `...`



demo演示：`对应上方Dockfile中的demo`

```yaml
 version: "3.9"
 services:
   fileserver:
     build: .
     image: fileserver
     volumes:
       - $PWD/FileResource:/root/FileResource
     ports:
       - "8000:8080"
```

#### 5.3 启动demo

```shell
docker-compose up .
```



### 6. 参考链接

具体命令参考docker官方文档

[Docker Desktop overview | Docker Documentation](https://docs.docker.com/desktop/)

微软docker教程

[教程：Windows 或 Mac 上的 Docker 和 Visual Studio Code 入门 | Microsoft Docs](https://docs.microsoft.com/zh-cn/visualstudio/docker/tutorials/docker-tutorial)



### 7. 常见问题汇总

1. 用户组权限问题

   ```shell
   Client: Docker Engine - Community
    Version:           20.10.12
    API version:       1.41
    Go version:        go1.16.12
    Git commit:        e91ed57
    Built:             Mon Dec 13 11:45:33 2021
    OS/Arch:           linux/amd64
    Context:           default
    Experimental:      true
   Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.24/version": dial unix /var/run/docker.sock: connect: permission denied
   ```

   解决方案

   ```shell
   # 将当前用户加入到docker用户组中
   sudo groupadd docker
   sudo gpasswd -a $USER docker
   newgrep docker
   ```

2. docker 常见时区设置

    ```shell
    ENV TZ Asia/ShangHai
    ```
   
3. docker compose组合服务间的ready控制问题

    相关文档[https://docs.docker.com/compose/startup-order/](https://docs.docker.com/compose/startup-order/)