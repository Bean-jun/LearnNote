"""
进程通信 pipe
"""

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
    # func_1-68802-发送数据:2022-08-14 16:36:06.287318
    # func_2-68803-接受数据:2022-08-14 16:36:06.287318
    # func_1-68802-发送数据:2022-08-14 16:36:07.295923
    # func_2-68803-接受数据:2022-08-14 16:36:07.295923
    # func_1-68802-发送数据:2022-08-14 16:36:08.297912
    # func_2-68803-接受数据:2022-08-14 16:36:08.297912
    # func_1-68802-发送数据:2022-08-14 16:36:09.300403
    # func_2-68803-接受数据:2022-08-14 16:36:09.300403
    # func_1-68802-发送数据:2022-08-14 16:36:10.306466
    # func_2-68803-接受数据:2022-08-14 16:36:10.306466
    # func_1-68802-发送数据:2022-08-14 16:36:11.307733
    # func_2-68803-接受数据:2022-08-14 16:36:11.307733
    # func_1-68802-发送数据:2022-08-14 16:36:12.309413
    # func_2-68803-接受数据:2022-08-14 16:36:12.309413
    # func_1-68802-发送数据:2022-08-14 16:36:13.315597
    # func_2-68803-接受数据:2022-08-14 16:36:13.315597
    # func_1-68802-发送数据:2022-08-14 16:36:14.318780
    # func_2-68803-接受数据:2022-08-14 16:36:14.318780
    # func_1-68802-发送数据:2022-08-14 16:36:15.325226
    # func_2-68803-接受数据:2022-08-14 16:36:15.325226
    # func_1-68802-发送数据:2022-08-14 16:36:16.330455
    # func_2-68803-接受数据:2022-08-14 16:36:16.330455
    # func_2-68803-发送数据:你是不是发送结束了？？？
    # func_1-68802-接受数据: 你是不是发送结束了？？？
    # 进程结束
