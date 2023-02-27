1. 时间相关

    ```python
    import pytz
    import time
    from datetime import datetime

    # 北京时间时区
    beijing = pytz.timezone("Asia/Shanghai")

    a = datetime.now(beijing)

    # 时间戳
    loc_timestamp = time.time()

    # 转utc时间 datetime.datetime 类型
    utc_date = datetime.utcfromtimestamp(loc_timestamp)

    # 转utc当地 标识的时间
    utc_loc_time = pytz.utc.localize(utc_date)
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'

    # 转北京时间
    beijing_time = utc_loc_time.astimezone(beijing)

    # utc 时间
    utc_time = beijing_time

    # cst时间
    cst_time = beijing_time.strftime(fmt)
    ```

2. 一个简单的爬虫

    ```python
    import os
    from datetime import datetime
    import requests
    from lxml import etree
    
    BASE_URL = "https://cn.bing.com"
    
    
    def get_response(url, n=2):
        """
        获取内容
        """
        if n <= 0:
            return
        try:
            header = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
            }
            if isinstance(url, str):
                response = requests.get(url, headers=header)
                yield response
            elif isinstance(url, list) or isinstance(url, tuple):
                for uri in url:
                    response = requests.get(uri, headers=header)
                    yield response
        except Exception as e:
            return get_response(url, n-1)
         
    def get_xpath_content(response, xpath, n=2):
        """
        获取xpath内容
        """
        if n <= 0:
            return
        try:
            _html = etree.HTML(response.text)
            res = _html.xpath(xpath)[0]
            return res
        except Exception as e:
            return get_xpath_content(response, xpath, n-1)
          
         
    def save_content(content):
        """
        保存内容
        """
        try:
            os.mkdir("bing")
        except Exception as e:
            pass
        filename = "bing/" + datetime.now().strftime("%Y-%m-%d-%H") + ".png"
        with open(filename, 'ab') as f:
            f.write(content.content)
            
           
    if __name__ == "__main__":
        xpath = "// *[@id='preloadBg']/@href"
        for response in get_response(BASE_URL):
            res = get_xpath_content(response, xpath)
            uri = BASE_URL + res
            for _response in get_response(uri):
                save_content(_response)
    ```

3. 图片压缩

    ```python
    import base64
    import io
    import os
    
    from PIL import Image, ImageFile
    
    
    # 压缩图片文件
    def compress_image(outfile, mb=900, quality=85, k=0.9):
        """不改变图片尺寸压缩到指定大小
        :param outfile: 压缩文件保存地址
        :param mb: 压缩目标，KB
        :param step: 每次调整的压缩比率
        :param quality: 初始压缩比率
        :return: 压缩文件地址，压缩文件大小
        """
    
        o_size = os.path.getsize(outfile) // 1024
        print(o_size, mb)
        if o_size <= mb:
            return outfile
    
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        while o_size > mb:
            im = Image.open(outfile)
            x, y = im.size
            out = im.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
            try:
                out.save(outfile, quality=quality)
            except Exception as e:
                print(e)
                break
            o_size = os.path.getsize(outfile) // 1024
        return outfile
      
      
    # 压缩base64的图片
    def compress_image_bs4(b64, mb=190, k=0.9):
        """不改变图片尺寸压缩到指定大小
        :param outfile: 压缩文件保存地址
        :param mb: 压缩目标，KB
        :param step: 每次调整的压缩比率
        :param quality: 初始压缩比率
        :return: 压缩文件地址，压缩文件大小
        """
        f = base64.b64decode(b64)
        with io.BytesIO(f) as im:
            o_size = len(im.getvalue()) // 1024
            if o_size <= mb:
                return b64
            im_out = im
            while o_size > mb:
                img = Image.open(im_out)
                x, y = img.size
                out = img.resize((int(x * k), int(y * k)), Image.ANTIALIAS)
                im_out.close()
                im_out = io.BytesIO()
                out.save(im_out, 'jpeg')
                o_size = len(im_out.getvalue()) // 1024
            b64 = base64.b64encode(im_out.getvalue())
            im_out.close()
            return str(b64, encoding='utf8')
    
     
    if __name__ == "__main__":
        for img in os.listdir('./out_img'):
            compress_image(outfile='./out_img/' + str(img)[0:-4] + '.png')
    ```


4. 连接mysql、redis

    ```python
    import redis
    import pymysql
    
    
    # redis
    pool = redis.ConnectionPool(host='localhost',port=6379, db=15)
    db = redis.Redis(connection_pool=pool)
    
    # mysql
    def connect_mysql(host="localhost", user="root", port=3306, password='', database=''):
        client = pymysql.connect(host=host,
                                user=user,
                                port=port,
                                password=password,
                                database=database)
        # cursor = client.cursor()
        return client
    ```


5. kill threading

    ```python
    import ctypes
    import inspect
    
    
    def _async_raise(tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            # _typeshed.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
            
    def stop_thread(thread):
        _async_raise(thread.ident, SystemExit)
    ```


6. custom flask logger

    ```python
    import logging
    import logging.config
    import logging.handlers
    import os
    import sys
    from datetime import date
    
    
    class Logger:
        def __init__(self, app=None, path="logs", fmt=None, level=logging.DEBUG):
            self.logger = logging.getLogger(__name__)
            self.level = level
            self.path = path
            if isinstance(fmt, logging.Formatter):
                self.fmt = fmt
            else:
                self.fmt = logging.Formatter(
                    "%(asctime)s [%(levelname)s] [%(threadName)s:%(thread)d] [%(module)s] [%(pathname)s:%(lineno)d] - %(message)s"
                )
    
            self.terminal = sys.stdout  # 将标准输出处理至终端
            self.logger.setLevel(level=self.level)  # 自定义日志器
            self.all_file_handler()
            self.errors_file_handler()
    
            if app is not None:
                self.init_app(app)
    
        def write(self, msg):
            self.terminal.write(msg)  # 将日志输出到终端
            if msg != "\n":
                self.logger.debug(msg)  # 日志写入文件中
    
        def flush(self):
            pass
    
        def init_app(self, app):
            app.logger = self.logger
    
        def exists_path(self, path=None):
            if not path:
                path = self.path
            return os.path.exists(path)
    
        def mkdir_path(self, path):
            if not self.exists_path(path):
                os.makedirs(path)
    
        def log_filename(self, prefix="log"):
            filename = "%s_%s%s" % (prefix, date.today().isoformat(), ".log")
            path = os.path.join(self.path, filename)
            return path
    
        def all_file_handler(self):
            self.mkdir_path(self.path)
            log_path = self.log_filename("all_log_")
            file = logging.handlers.RotatingFileHandler(log_path, maxBytes=10485760, backupCount=20, encoding="utf-8")
            file.setFormatter(self.fmt)
            file.setLevel(logging.DEBUG)
            self.logger.addHandler(file)
    
        def errors_file_handler(self):
            self.mkdir_path(self.path)
            log_path = self.log_filename("error_log_")
            file = logging.handlers.RotatingFileHandler(log_path, maxBytes=10485760, backupCount=20, encoding="utf-8")
            file.setFormatter(self.fmt)
            file.setLevel(logging.ERROR)
            self.logger.addHandler(file)
            
            
    def init_app(app):
        logger = Logger()
        logger.init_app(app)
    
        sys.stdout = logger
    ```
    
    
7. Uncompress zip file

    ```python
    import os
    import zipfile

    def decode_to_plain_text(text):
        try:
            text = text.encode('cp437').decode('gbk')
        except:
            text = text.encode('cp437').decode('utf-8')
        return text

    def abs_path(base_dir, dir):
        return os.path.join(base_dir, dir)

    def unzip_to(zip_file, dest_dir):
        with zipfile.ZipFile(zip_file) as packages:
            packages.extractall(dest_dir)
            folder_dict = {}
            for dirpath, dirnames, filenames in os.walk(dest_dir):
                for filename in filenames:
                    new_filename = decode_to_plain_text(filename)
                    os.rename(os.path.join(dirpath, filename),
                            os.path.join(dirpath, new_filename))
                for dirname in dirnames:
                    new_dirname = decode_to_plain_text(dirname)
                    if dirname == new_dirname:
                        continue
                    folder_dict[abs_path(dirpath, dirname)] = abs_path(dirpath, new_dirname)
            # 修改文件夹名称
            folder_list = sorted(folder_dict.items(), key=lambda x: len(x[0].split(os.sep)), reverse=True)
            for old_file, new_file in folder_list:
                os.rename(old_file, new_file)
    ```


