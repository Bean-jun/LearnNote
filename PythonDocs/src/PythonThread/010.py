import threading
import time


def showMsg():
    print("前面的准备工作都做完了,开始我自己的事情..")


barrier = threading.Barrier(3, showMsg)


def func(i):
    # time.sleep(4)
    print(i, "执行准备工作")
    # 设置超时时间，如果超时，没有达到障碍线程数量，
    # 会进入断开状态，引发BrokenBarrierError错误
    try:
        barrier.wait(10)
    except Exception as e:
        print(e)
    print("current task id:", i)


def main():
    for i in range(3):
        t = threading.Thread(target=func, args=(i, ))
        t.start()

        # 当然 我们也可以将之前的wait结果给恢复至初始状态
        if i == 1:
            barrier.reset()


if __name__ == "__main__":
    main()
