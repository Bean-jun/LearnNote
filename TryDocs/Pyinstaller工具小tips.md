# pyinstaller打包小技巧

1. 单py文件打包

    ```shell
    pyinstaller -F xxx.py
    ```

2. 含有其他依赖文件的打包

- 代码相关层面的修改
    ```shell
    由于项目代码依赖外部文件，而打包之后的二进制执行文件会在系统的临时文件系统中操作，故需要做特殊处理
    ```

    ```python
    # 项目未打包时，对于外部库的调用可以这样简单的描述, libs是我目前存放外部库的文件夹
    import os
    bin_path = os.path.join(os.getcwd(), "libs", "我是外部库.exe")
    os.system(bin_path)

    # 但是项目一旦打包，当前获取的bin_path路径是当前二进制文件所在路径拼接的地址，而pyinstaller打包解压后的文件存档在系统的临时目录中，需要通过 sys._MEIPASS获取，相关公共代码如下:

    def resource_path(relative_path):
        if getattr(sys, 'frozen', False): #是否Bundle Resource
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    # 此时相关代码调用如下：
    # resource_path("libs")找到的才是当前被打包之后的外部库的真实地址
    bin_path = os.path.join(resource_path("libs"), "我是外部库.exe")
    os.system(bin_path)
    ```

- 打包相关层面的操作

    ```shell
    # 1. 生成打包时的spec文件
    # --onefile 单文件
    # --add-data libs;libs 表示添加对应的文件夹到需要打包的环境中
    # --icon static\\icon.ico 打包之后的logo
    # -n 项目打包后的别名

    pyi-makespec --console --onefile --add-data libs;libs --icon static\\icon.ico xxx.py -n build_filename

    # 2. 执行相关命令进行打包
    pyinstaller build_filename.spec
    ```