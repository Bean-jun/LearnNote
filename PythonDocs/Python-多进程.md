### 一、多进程基础

1. 创建一个多进程并启动进程

    方式一【基于multiprocessing模块的创建】：

    ```python
    # src/PythonProcess/001.py
    import multiprocessing
    import os


    def func(num):
        print("当前获取数字：", num, "当前获取进程ID: ", os.getpid())


    def main():
        tasks = []
        for i in range(10):
            p = multiprocessing.Process(target=func, args=(i,))
            tasks.append(p)

        [p.start() for p in tasks]

        [p.join() for p in tasks]

        print("进程结束")


    if __name__ == "__main__":
        main()
    ```

    方式二【通过对multiprocessing模块Process的继承的创建】：

    ```python
    # src/PythonProcess/002.py
    import multiprocessing
    import os


    class ProcessChild(multiprocessing.Process):

        def __init__(self, group=None, target=None, name=None, args=()):
            super().__init__(group=group, target=target, name=name, args=args)

        def run(self):
            print("当前获取数字：", self._args, "当前获取进程ID: ", os.getpid())


    def main():
        tasks = []
        for i in range(10):
            tasks.append(ProcessChild(args=(i, )))

        [i.start() for i in tasks]

        [i.join() for i in tasks]

        print("进程结束")


    if __name__ == "__main__":
        main()
    ```

2. 进程相关函数

    同线程, 见文档[https://docs.python.org/zh-cn/3/library/multiprocessing.html](https://docs.python.org/zh-cn/3/library/multiprocessing.html)


### 二、进程同步

1. Demo

    ```python
    # src/PythonProcess/003.py
    import multiprocessing
    import os


    def func(l, num):
        with l:
            print("当前获取到的数据结果为: ", num, "当前进程ID: ", os.getpid())


    def main():
        l = multiprocessing.Lock()
        tasks = []
        for i in range(10):
            p = multiprocessing.Process(target=func, args=(l, i))
            # p = multiprocessing.Process(target=func, args=(i,))
            tasks.append(p)

        [p.start() for p in tasks]

        [p.join() for p in tasks]

        print("进程结束")


    if __name__ == "__main__":
        main()
    ```

### 三、进程通信

1. Queue通信

    ```python
    # src/PythonProcess/004.py
    from multiprocessing import Process, Queue
    import datetime
    import os
    import time


    def func_1(q):
        n = 10
        while True:
            if n < 0:
                break
            msg = datetime.datetime.now()
            print("func_1-"+str(os.getpid())+"-发送数据:"+str(msg))
            q.put(msg)
            time.sleep(1)
            n -= 1


    def func_2(q):
        try:
            while True:
                ret = q.get(timeout=5)
                print("func_2-"+str(os.getpid())+"-接受数据:"+str(ret))
        except Exception as e:
            print(e.args)


    def main():
        q = Queue(10)
        tasks = []
        for _ in range(2):
            if _ == 0:
                p = Process(target=func_1, args=(q,))
            else:
                p = Process(target=func_2, args=(q,))
            tasks.append(p)

        [p.start() for p in tasks]

        [p.join() for p in tasks]

        print("进程结束")


    if __name__ == "__main__":
        main()
        # func_1-60058-发送数据:2022-08-14 16:15:21.445148
        # func_2-60059-接受数据:2022-08-14 16:15:21.445148
        # func_1-60058-发送数据:2022-08-14 16:15:22.454947
        # func_2-60059-接受数据:2022-08-14 16:15:22.454947
        # func_1-60058-发送数据:2022-08-14 16:15:23.457649
        # func_2-60059-接受数据:2022-08-14 16:15:23.457649
        # func_1-60058-发送数据:2022-08-14 16:15:24.463014
        # func_2-60059-接受数据:2022-08-14 16:15:24.463014
        # func_1-60058-发送数据:2022-08-14 16:15:25.464202
        # func_2-60059-接受数据:2022-08-14 16:15:25.464202
        # func_1-60058-发送数据:2022-08-14 16:15:26.467098
        # func_2-60059-接受数据:2022-08-14 16:15:26.467098
        # func_1-60058-发送数据:2022-08-14 16:15:27.468392
        # func_2-60059-接受数据:2022-08-14 16:15:27.468392
        # func_1-60058-发送数据:2022-08-14 16:15:28.473154
        # func_2-60059-接受数据:2022-08-14 16:15:28.473154
        # func_1-60058-发送数据:2022-08-14 16:15:29.475600
        # func_2-60059-接受数据:2022-08-14 16:15:29.475600
        # func_1-60058-发送数据:2022-08-14 16:15:30.476320
        # func_2-60059-接受数据:2022-08-14 16:15:30.476320
        # func_1-60058-发送数据:2022-08-14 16:15:31.477738
        # func_2-60059-接受数据:2022-08-14 16:15:31.477738
        # ()
        # 进程结束
    ```

2. Pipe通信

    Pipe() 函数返回一个由管道连接的连接对象，默认情况下是双工（双向）。Pipe() 表示管道的两端。每个连接对象都有 send() 和 recv() 方法（相互之间的）。请注意，如果两个进程（或线程）同时尝试读取或写入管道的 同一 端，则管道中的数据可能会损坏。当然，在不同进程中同时使用管道的不同端的情况下不存在损坏的风险。

```python
# src/PythonProcess/005.py
from multiprocessing import Process, Pipe
import datetime
import os
import time


def func_1(p):

    n = 10
    while True:
        if n < 0:
            break
        msg = datetime.datetime.now()
        print("func_1-"+str(os.getpid())+"-发送数据:"+str(msg))
        p.send(msg)
        time.sleep(1)
        n -= 1
    try:
        time.sleep(10)
        print("func_1-"+str(os.getpid())+"-接受数据:", p.recv())
    except Exception as e:
        print(e.args, "func_1")


def func_2(p):
    n = 10
    try:
        while True:
            if n < 0:
                break
            ret = p.recv()
            print("func_2-"+str(os.getpid())+"-接受数据:"+str(ret))
            n -= 1
    except Exception as e:
        print(e.args)
    else:
        msg = "你是不是发送结束了？？？"
        print("func_2-"+str(os.getpid())+"-发送数据:"+str(msg))
        p.send(msg)


def main():
    l_p, r_p = Pipe()
    tasks = []
    for _ in range(2):
        if _ == 0:
            p = Process(target=func_1, args=(l_p,))
        else:
            p = Process(target=func_2, args=(r_p,))
        tasks.append(p)

    [p.start() for p in tasks]

    [p.join() for p in tasks]

    print("进程结束")


if __name__ == "__main__":
    main()
```

3. 管理器共享进程状态

    [https://docs.python.org/zh-cn/3/library/multiprocessing.html#sharing-state-between-processes](https://docs.python.org/zh-cn/3/library/multiprocessing.html#sharing-state-between-processes)
