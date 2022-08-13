from datetime import datetime
import threading


def func():
    print("current time: ", datetime.now())


def func2():
    print("current time: ", datetime.now())
    timer = threading.Timer(2, func2)
    timer.start()


def main():
    print("start....")
    # timer = threading.Timer(10, func) # 定时执行一次
    timer = threading.Timer(10, func2)  # 函数内部有定时任务，故不间断执行
    timer.start()


if __name__ == "__main__":
    main()
