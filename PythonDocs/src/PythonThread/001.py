import threading


def func(num):
    print("当前获取数字：", num)


def main():
    tasks = []
    for i in range(10):
        tasks.append(threading.Thread(target=func, args=(i, )))

    [i.start() for i in tasks]

    [i.join() for i in tasks]

    print("线程结束")


if __name__ == "__main__":
    main()
    # 当前获取数字： 0
    # 当前获取数字： 1
    # 当前获取数字： 2
    # 当前获取数字： 4
    # 当前获取数字： 5
    # 当前获取数字： 6
    # 当前获取数字： 3
    # 当前获取数字： 7
    # 当前获取数字： 9
    # 当前获取数字： 8
    # 线程结束
