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
    # 当前获取数字： 0 当前获取进程ID:  34007
    # 当前获取数字： 1 当前获取进程ID:  34008
    # 当前获取数字： 2 当前获取进程ID:  34009
    # 当前获取数字： 3 当前获取进程ID:  34010
    # 当前获取数字： 5 当前获取进程ID:  34012
    # 当前获取数字： 9 当前获取进程ID:  34016
    # 当前获取数字： 6 当前获取进程ID:  34013
    # 当前获取数字： 4 当前获取进程ID:  34011
    # 当前获取数字： 8 当前获取进程ID:  34015
    # 当前获取数字： 7 当前获取进程ID:  34014
    # 进程结束
