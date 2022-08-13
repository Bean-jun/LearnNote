import threading

"""
模拟线程通信,两个线程交替输出1-10
"""
con = threading.Condition()
number = 1


def func_1():
    global number

    # 获得锁
    con.acquire()
    while True:
        print(f"current thread {threading.current_thread().name} print: {number}")
        number += 1
        # 自己开始阻塞&等待被唤醒
        con.wait()
        con.notify()

        if number > 10:
            break

    con.release()


def func_2():
    global number

    # 获得锁
    con.acquire()
    while True:
        # 等待被唤醒
        print(f"current thread {threading.current_thread().name} print: {number}")
        number += 1
        # 唤醒另一个线程 & 自己开始阻塞
        con.notify()
        con.wait()

        if number > 10:
            break
    con.release()


def main():
    f1 = threading.Thread(target=func_1)
    f2 = threading.Thread(target=func_2)

    f1.start()
    f2.start()

    # 默认主线程等待子线程执行完毕，故不做任何操作


if __name__ == "__main__":
    main()
    # current thread Thread-1 (func_1) print: 1
    # current thread Thread-2 (func_2) print: 2
    # current thread Thread-1 (func_1) print: 3
    # current thread Thread-2 (func_2) print: 4
    # current thread Thread-1 (func_1) print: 5
    # current thread Thread-2 (func_2) print: 6
    # current thread Thread-1 (func_1) print: 7
    # current thread Thread-2 (func_2) print: 8
    # current thread Thread-1 (func_1) print: 9
    # current thread Thread-2 (func_2) print: 10