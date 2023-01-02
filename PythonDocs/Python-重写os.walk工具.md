1. 心血来潮，仿写一个pythond os.walk工具

```python
# PythonDocs/src/027.py
import time
import os
from contextlib import contextmanager


@contextmanager
def to_folder(path):
    oldpath = os.getcwd()
    try:
        os.chdir(path)
        yield oldpath
    finally:
        os.chdir(oldpath)


def walk(path=".", exclude=None):
    if exclude is None:
        exclude = []

    global_folders = []

    def __func(path):
        dirpath = os.getcwd()
        folders = []
        filenames = []

        to_path = os.path.join(dirpath, path)
        with to_folder(to_path):
            dirpath = os.getcwd()
            for folder_or_file in os.listdir(path):
                if folder_or_file in exclude:
                    continue
                if os.path.isdir(os.path.join(to_path, folder_or_file)):
                    folders.append(folder_or_file)
                    global_folders.append(os.path.join(to_path,
                                                       folder_or_file))
                else:
                    filenames.append(folder_or_file)
            return dirpath, folders, filenames

    yield __func(path)

    for folder in global_folders:
        yield __func(folder)


exclude = ['.git', ".env"]

node01 = time.time()
for dirpath, folders, filenames in os.walk("."):
    # print(dirpath, folders, filenames)
    pass
node02 = time.time()
for dirpath, folders, filenames in walk(exclude=exclude):
    # print(dirpath, folders, filenames)
    pass
node03 = time.time()
print(node02-node01, node03-node02)
```

2. 扫描结果

```shell
MyLearnGuide ['.static', 'BugDocs', 'DatabaseDocs', 'DeployDocs', 'DesignDocs', 'DevelopDocs', 'FrontDocs', 'GolangDocs', 'NetworkDocs', 'OtherDocs', 'PythonDocs', 'ToolsDocs', 'TryDocs', 'WebFrameDocs'] ['.gitignore', '.nojekyll', 'index.html', 'LICENSE', 'README.md']
MyLearnGuide\.static ['css', 'js'] []
MyLearnGuide\BugDocs ['cookies'] []
MyLearnGuide\DatabaseDocs [] ['MySQL-入门.md', 'Redis-事务.md', 'Redis-入门.md', 'Redis-持久化.md']
MyLearnGuide\DeployDocs [] ['nginx_uwsgi_django部署.md', 'nginx_uwsgi_flask部署.md']
MyLearnGuide\DesignDocs ['src'] ['设计模式.md']
MyLearnGuide\DevelopDocs ['images'] ['cookie_session_token介绍.md', 'LVS介绍.md', 'oauth2_sso介绍.md']
MyLearnGuide\FrontDocs ['image'] ['Ajax-基础语法.md', 'CSS-基础语法.md', 'HTML-基础语法.md', 'JavaScript-基础语法.md', 'JQuery-基础语法.md']
MyLearnGuide\GolangDocs ['src'] ['Golang-基础语法.md']
MyLearnGuide\NetworkDocs ['image', 'src'] ['基于Socket的HTTP协议实现.md', '基于Socket的TCP协议实现.md', '基于Socket 的UDP协议实现.md', '基于Socket的WebSocket协议实现.md', '结合SocketServer库的WebSocket协议实现.md']
MyLearnGuide\OtherDocs ['image'] ['celery使用.md', 'crontab.md', 'docker.md', 'nginx.md', 'nginx安装-Ubuntu.md', 'SQLAlchemy基本使用.md']
MyLearnGuide\PythonDocs ['src'] ['Python-上下文.md', 'Python-基础语法.md', 'Python-多线程.md', 'Python-多进程.md', 'Python-常见代码.md', 'Python-理解元类.md', 'Python-生成器&迭代器&迭代对象.md', 'Python-重写os.walk工具.md', 'Python-闭包&装饰器.md']      
MyLearnGuide\ToolsDocs ['src'] ['工具集合.md']
MyLearnGuide\TryDocs [] ['Jetson_Nano_环境搭建.md']
MyLearnGuide\WebFrameDocs ['image', 'src'] ['Django-入门.md', 'DRF-入门.md', 'Flask-信号的使用.md', 'Flask-入门.md', 'Flask-源码分析.md']
MyLearnGuide\.static\css [] ['dark.min.css', 'pure.min.css', 'vue.min.css']
MyLearnGuide\.static\js [] ['docsify.min.js', 'prism-bash.min.js', 'prism-go.min.js', 'prism-javascript.min.js', 'prism-python.min.js', 'prism-sql.min.js']
MyLearnGuide\BugDocs\cookies ['image', 'src'] ['cookie离谱的生效范围.md']
MyLearnGuide\DesignDocs\src [] ['abstract_factory.py', 'factory_builder.py', 'factory_factory.py', 'factory_prototype.py']
MyLearnGuide\DevelopDocs\images [] ['2022-11-27-20-03-21.png', '2022-11-27-20-03-44.png', '2022-11-27-20-03-59.png', '2022-11-27-20-04-14.png', 'oauth2流程图.png', 'oauth_客户端模式.png', 'oauth_密码模式.png', 'oauth_授权码模式.png', 'oauth_简化模式.png']
MyLearnGuide\FrontDocs\image [] ['table_exercise.png']
MyLearnGuide\GolangDocs\src [] ['001.go', '002.go', '003.go', '004.go', '005.go', '006.go', '007.go', '008.go', '009.go', '010.go', '011.go', '012.go', '013.go', '014.go', '015.go', '016.go', '017.go', '018.go', '019.go', '020.go']
MyLearnGuide\NetworkDocs\image [] ['1538030297-3779-20150904110054856-961661137-20210905230123871.png', '1538030297-7824-20150904110008388-1768388886.gif', '2012072810301161.png', '867021-20180322001744323-654009411.jpg', 'image-20210912111134961.png', 'image-20210912111153729.png']
MyLearnGuide\NetworkDocs\src ['HTTP', 'TCP', 'UDP', 'WebSocket'] []
MyLearnGuide\OtherDocs\image ['celery', 'nginx安装-Ubuntu'] []
MyLearnGuide\PythonDocs\src ['PythonMetaClass', 'PythonProcess', 'PythonThread'] ['001.py', '002.py', '003.py', '004.py', '005.py', '006.py', '007.py', '008.py', '009.py', '010.py', '011.py', '012.py', '013.py', '014.py', '015.py', '016.py', '017.py', '018.py', '019.py', '020.py', '021.py', '022.py', '023.py', '024.py', '025.py', '026.py', '027.py', 'cache.py', 'log.txt']
MyLearnGuide\ToolsDocs\src [] ['vimrc.vimrc']
MyLearnGuide\WebFrameDocs\image [] ['image-20211003210113038.png']
MyLearnGuide\WebFrameDocs\src ['demo', 'flask'] ['flask_signal.py']
MyLearnGuide\BugDocs\cookies\image [] ['2022-09-19_21-50-59屏幕截图.png', '2022-09-19_21-51-14屏幕截图.png']        
MyLearnGuide\BugDocs\cookies\src ['templates'] ['app01.py', 'app02.py']
MyLearnGuide\NetworkDocs\src\HTTP [] ['file_server.py', 'server.py']
MyLearnGuide\NetworkDocs\src\TCP [] ['client.py', 'server.py']
MyLearnGuide\NetworkDocs\src\UDP [] ['recv.py', 'send.py']
MyLearnGuide\NetworkDocs\src\WebSocket [] ['server.py', 'T_WebSocket.html']
MyLearnGuide\OtherDocs\image\celery [] ['2314234123.jpeg', '3.png', 'celery_512.png']
MyLearnGuide\OtherDocs\image\nginx安装-Ubuntu [] ['image-20211128145308231.png']
MyLearnGuide\PythonDocs\src\PythonMetaClass [] ['fields.py', 'orm.py']
MyLearnGuide\PythonDocs\src\PythonProcess [] ['001.py', '002.py', '003.py', '004.py', '005.py']
MyLearnGuide\PythonDocs\src\PythonThread [] ['001.py', '002.py', '003.py', '004.py', '005.py', '006.py', '007.py', '008.py', '009.py', '010.py', '011.py']
MyLearnGuide\WebFrameDocs\src\demo ['flask-demo'] ['flask-demo-api.md']
MyLearnGuide\WebFrameDocs\src\flask [] ['local.py']
MyLearnGuide\BugDocs\cookies\src\templates [] ['index.html']
MyLearnGuide\WebFrameDocs\src\demo\flask-demo ['apps', 'conf', 'middleware'] ['app.py', 'requirments.txt']
MyLearnGuide\WebFrameDocs\src\demo\flask-demo\apps ['api'] ['models.py', '__init__.py']
MyLearnGuide\WebFrameDocs\src\demo\flask-demo\conf [] ['settings.py']
MyLearnGuide\WebFrameDocs\src\demo\flask-demo\middleware [] ['auth.py']
MyLearnGuide\WebFrameDocs\src\demo\flask-demo\apps\api ['common', 'resource'] ['__init__.py']
MyLearnGuide\WebFrameDocs\src\demo\flask-demo\apps\api\common [] ['response.py']
MyLearnGuide\WebFrameDocs\src\demo\flask-demo\apps\api\resource [] ['account.py', 'Base.py', 'home.py']
```