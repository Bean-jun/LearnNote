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

"""
加锁和不加锁的区别：

# 加锁打印输出：

当前获取到的数据结果为:  0 当前进程ID:  45462
当前获取到的数据结果为:  2 当前进程ID:  45465
当前获取到的数据结果为:  7 当前进程ID:  45470
当前获取到的数据结果为:  3 当前进程ID:  45466
当前获取到的数据结果为:  6 当前进程ID:  45469
当前获取到的数据结果为:  5 当前进程ID:  45468
当前获取到的数据结果为:  1 当前进程ID:  45464
当前获取到的数据结果为:  9 当前进程ID:  45472
当前获取到的数据结果为:  8 当前进程ID:  45471
当前获取到的数据结果为:  4 当前进程ID:  45467
进程结束

# 不加锁打印输出：

当前获取到的数据结果为:  7 当前进程ID:  45861
当前获取到的数据结果为:  1 当前进程ID:  45855
当前获取到的数据结果为: 当前获取到的数据结果为:  3 当前进程ID:  45857
 2 当前进程ID:  45856
当前获取到的数据结果为:  4 当前进程ID:  45858
当前获取到的数据结果为: 当前获取到的数据结果为:  0 当前进程ID:   458546
 当前进程ID:  45860
当前获取到的数据结果为:  5 当前进程ID:  45859
当前获取到的数据结果为:  8 当前进程ID:  45862
当前获取到的数据结果为:  9 当前进程ID:  45863
进程结束
"""