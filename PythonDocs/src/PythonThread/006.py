import threading
import time

event = threading.Event()


def task(i):
    print(
        f"start current ID: {i}, current thread status: {event.is_set()}")
    # 阻塞线程
    event.wait()
    # 执行结果
    print(
        f"end current ID: {i}, current thread status: {event.is_set()}")


def main():
    thread_task = list()
    for i in range(10):
        t = threading.Thread(target=task, args=(i, ))
        t.start()
        thread_task.append(t)

    time.sleep(3)
    # 由于task中设置的wait, 故当前线程执行一部分代码后都处于阻塞状态
    # 现在将线程状态释放
    event.set()


if __name__ == "__main__":
    main()
    """ result
    start current ID: 0, current thread status: False
    start current ID: 1, current thread status: False
    start current ID: 2, current thread status: False
    start current ID: 3, current thread status: False
    start current ID: 4, current thread status: False
    start current ID: 5, current thread status: False
    start current ID: 6, current thread status: False
    start current ID: 7, current thread status: False
    start current ID: 8, current thread status: False
    start current ID: 9, current thread status: False
    end current ID: 0, current thread status: True
    end current ID: 2, current thread status: True
    end current ID: 3, current thread status: True
    end current ID: 4, current thread status: True
    end current ID: 6, current thread status: True
    end current ID: 8, current thread status: True
    end current ID: 5, current thread status: True
    end current ID: 7, current thread status: True
    end current ID: 1, current thread status: True
    end current ID: 9, current thread status: True
    """