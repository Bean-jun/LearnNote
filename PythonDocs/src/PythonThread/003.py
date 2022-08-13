import time
import threading


def func(num):
    time.sleep(num)
    print("当前获取数字：", num)


def main():
    task1 = threading.Thread(target=func, args=(10, ))

    task1.daemon = True # 将线程设置为守护线程，有些地方写setDaemon(要被弃用啦)，也是一样的，但是建议直接写daemon哦

    task1.start()
    # task1.join()

    print("线程结束")


if __name__ == "__main__":
    main()
