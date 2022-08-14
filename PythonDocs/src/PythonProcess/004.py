"""
进程通信 queue
"""

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
