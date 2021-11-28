### 一、下载

打开这个网站下载对应包即可，一般用最新版就好~

地址：[https://nginx.org/en/download.html](https://nginx.org/en/download.html)

![image-20211128145308231](image/nginx安装-Ubuntu/image-20211128145308231.png)

Ubuntu下，直接复制上图中左边框住的地址链接，然后....，使用`terminal`开始吧~

```shell
wget https://nginx.org/download/nginx-1.20.2.tar.gz
```



### 二、安装

1. 解压

   ```shell
   tar -xvf nginx-1.20.2.tar.gz
   ```

	2. 进入解压目录

    ```shell
    cd nginx-1.20.2
    ```

	3. 安装依赖

    请务必安装，否则在编译时会出错哦，这样就没办法正常安装软件了，直接一下子上就好....

    ```shell
    # 更新
    sudo apt update
    sudo apt upgrade
    # 安装依赖
    sudo apt install glibc-devel	# 一般这个显示缺少
    sudo apt install build-essential
    sudo apt install libpcre3 libpcre3-dev	# 一般这个显示缺少
    sudo apt install zlib1g-dev	# 一般这个显示缺少
    sudo apt install openssl	# 一般这个显示缺少
    ```

	4. 编译

    ```shell
    # 若是不配置什么的，这个就够了
    ./configure
    ```

	5. 安装

    ```shell
    sudo make && make install
    ```



### 三、测试

默认安装目录：

```shell
/usr/local/nginx
```

尝试启动

```shell
sudo /usr/local/nginx/sbin/nginx
```

打开浏览器输入对应ip查看....



### 四、其他

Ubuntu 下更简单的安装方式

```shell
sudo apt install nginx
```

额......