### 一、多线程基础

1. 创建一个多线程并启动线程

    引用多线程理由:我想让电脑做很多事情....

    方式一【基于threading模块的创建】：

    ```python
    # src/PythonThread/001.py
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
    ```

    方式二【通过对threading模块Thread的继承的创建】：

    ```python
    # src/PythonThread/002.py
    import threading

    def func(num):
        print("当前获取数字：", num)

    class ThreadChild(threading.Thread):

        def __init__(self, target, name, args):
            super().__init__(target=target, name=name, args=args)

        def run(self):
            print("当前线程名：", self.getName)
            return super().run()

    def main():
        tasks = []
        for i in range(10):
            tasks.append(ThreadChild(target=func, name=f"name-{i}", args=(i, )))

        [i.start() for i in tasks]

        [i.join() for i in tasks]

        print("线程结束")

    if __name__ == "__main__":
        main()
    ```

2. 线程相关函数

    2.1 threading.Thread — 创建线程并初始化线程，可以为线程传递参数 ；

    2.2 threading.enumerate — 返回一个包含正在运行的线程的list；

    2.3 threading.activeCount — 返回正在运行的线程数量，与len(threading.enumerate)有相同的结果；

    2.4 Thread.start — 启动线程 ；

    2.5 Thread.join — 阻塞函数，一直等到线程结束为止；注意：它将阻塞主线程 ；见src/PythonThread/003.py

    2.6 Thread.isAlive — 返回线程是否活动的；

    2.7 Thread.getName — 返回线程名；

    2.8 Thread.setName — 设置线程名；

    2.9 Thread.setDaemon - (daemon)设置为后台线程 default False 设置在start 之前;设置为 True 之后则主线程不会再等待子线程结束才结束，而是主线程结束意味程序退出，子线程也立即结束；见src/PythonThread/003.py


### 二、线程互斥锁 Lock

引用理由：线程可以通过共享变量完成通信，但总是会出现一些奇怪的问题.保证数据的正常修改和访问

1. 创建多线程任务，同时对全局变量进行操作

    ```python
    # src/PythonThread/004.py
    import threading

    NUM = 100

    def task1(n):
        global NUM
        for i in range(n):
            NUM = NUM + 1

    def task2(n):
        global NUM
        for i in range(n):
            NUM = NUM - 1

    def main():
        t1 = threading.Thread(target=task1, name="name-task1", args=(10000000, ))
        t2 = threading.Thread(target=task2, name="name-task1", args=(10000000, ))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print(f"NUM预期结果:100, 最终结果:{NUM}")

    if __name__ == "__main__":
        main()
    ```

    嗯？操作结果看起来很正常哇，没有奇怪的问题啊？？？？？咋费事？？？？？请看后续GIL【挖坑】

2. 线程互斥锁

    在python中通过threading.Lock创建锁

    ```python
    # src/PythonThread/005.py
    import threading

    lock = threading.Lock()

    NUM = 100

    def task1(n):
        global NUM
        for i in range(n):
            with lock:  # 使用with语句也可以
                # lock.acquire()
                NUM += i
                # lock.release()

    def task2(n):
        global NUM
        for i in range(n):
            lock.acquire()
            NUM -= i
            lock.release()

    def main():
        t1 = threading.Thread(target=task1, name="name-task1", args=(1000, ))
        t2 = threading.Thread(target=task2, name="name-task1", args=(1000, ))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print(f"NUM预期结果:100, 最终结果:{NUM}")

        print("线程结束")

    if __name__ == "__main__":
        main()
    ```


### 三、线程事件 Event

事件 event 中有一个全局内置标志 Flag，值为 True 或者False。使用 wait 函数的线程会处于阻塞状态,此时 Flag 指为 False，直到有其他线程调用 set 函数让全局标志 Flag 置为 True ，其阻塞的线程立刻恢复运行，还可以用 isSet 函数检查当前的 Flag 状态.

1. Event函数介绍

    1.1 set — 全局内置标志 Flag，将标志 Flag 设置为 True,通知在等待状态 ( wait ) 的线程恢复运行

    1.2 isSet — 获取标志 Flag 当前状态，返回 True 或者 False

    1.3 wait — 一旦调用，线程将会处于阻塞状态，直到等待其他线程调用 set 函数恢复运行

    1.4 clear — 将标志设置为False

2. Demo

    ```python
    # src/PythonThread/006.py
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
    ```


### 四、线程条件变量 Condition

Condition 提供了一种多线程通信机制，假如线程 1 需要数据，那么线程 1 就阻塞等待，这时线程 2 就去制造数据，线程 2 制造好数据后，通知线程 1 可以去取数据了，然后线程 1 去获取数据

1. Condition函数介绍

    1.1 acquire —  线程锁，注意线程条件变量 Condition 中的所有相关函数使用必须在acquire / release 内部操作
    
    1.2 release — 释放锁，注意线程条件变量 Condition 中的所有相关函数使用必须在acquire / release 内部操作

    1.3 wait( timeout ) —  线程挂起(阻塞状态)，直到收到一个 notify 通知或者超时才会被唤醒继续运行（超时参数默认不设置，可选填，类型是浮点数，单位是秒）wait 必须在已获得 Lock 前提下才能调用，否则会触发 RuntimeError;调用时，将释放底层锁，而且线程将进入睡眠状态，直到另一个线程在条件变量上执行notify()或notify_all()方法将其唤醒为止。在线程被唤醒后，线程讲重新获取锁，方法也会返回。

    1.4 notify(n=1) —  通知其他线程，那些挂起的线程接到这个通知之后会开始运行，缺省参数，默认是通知一个正等待通知的线程,最多则唤醒 n 个等待的线程。 notify 必须在已获得 Lock 前提下才能调用，否则会触发 RuntimeError,notify 不会主动释放 Lock

    1.5 notifyAll —  如果wait状态线程比较多，notifyAll 的作用就是通知所有线程

2. Demo

    ```python
    # src/PythonThread/007.py
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
    ```

### 五、线程定时器 Timer

指定时间间隔后启动线程

1. Timer官方解释说明

    ```python
    """Call a function after a specified number of seconds:
    t = Timer(30.0, f, args=None, kwargs=None)
    t.start()
    t.cancel()     # stop the timer's action if it's still waiting
    """
    ```

2. Demo

    ```python
    # src/PythonThread/008.py
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
    ```

### 六、线程信号量 Semaphore

信号量可以通过内置计数器来控制同时运行线程的数量，启动线程(消耗信号量)内置计数器会自动减一，线程结束(释放信号量)内置计数器会自动加一；内置计数器为零，启动线程会阻塞，直到有本线程结束或者其他线程结束为止

1. Demo

    ```python
    # src/PythonThread/009.py
    from datetime import datetime
    import threading
    import time

    sem = threading.Semaphore(4)

    def func(id):
        sem.acquire()
        print(str(id) + " thread id:",
            threading.current_thread().ident,
            "current time:",
            datetime.now())
        time.sleep(3)
        sem.release()
        # 或者这样写
        # with sem:
        #     print(str(id) + "thread id:",
        #           threading.currentThread().ident,
        #           "current time:",
        #           datetime.now())
        #     time.sleep(3)

    def main():
        for i in range(10):
            t = threading.Thread(target=func, args=(i, ))
            t.start()

    if __name__ == "__main__":
        main()
        # 0 thread id: 123145618636800 current time: 2022-08-11 23:41:49.066956
        # 1 thread id: 123145635426304 current time: 2022-08-11 23:41:49.070871
        # 2 thread id: 123145652215808 current time: 2022-08-11 23:41:49.074061
        # 3 thread id: 123145669005312 current time: 2022-08-11 23:41:49.077171
        # 4 thread id: 123145685794816 current time: 2022-08-11 23:41:52.069284
        # 5 thread id: 123145702584320 current time: 2022-08-11 23:41:52.072310
        # 6 thread id: 123145719373824 current time: 2022-08-11 23:41:52.077007
        # 7 thread id: 123145736163328 current time: 2022-08-11 23:41:52.080037
        # 8 thread id: 123145752952832 current time: 2022-08-11 23:41:55.070314
        # 9 thread id: 123145769742336 current time: 2022-08-11 23:41:55.076489
    ```


### 七、线程栅栏 Barrier

Barrier 栅栏对象，多线程 Barrier 会设置一个线程栅栏数量 parties ，如果等待的线程数量没有达到栅栏数量 parties ，所有线程会处于阻塞状态，当等待的线程到达了这个数量就会唤醒所有的等待线程。用于应对固定数量的线程需要彼此相互等待的情况

1. Barrier函数介绍

    1.1 wait(timeout=None)  阻塞并尝试通过栅栏，如果等待的线程数量大于或者等于线程栅栏数量 parties ，则表示栅栏通过，执行 action 对应函数并执行线程内部代码，反之则继续等待；如果 wait(timeout=None)  等待超时，栅栏将进入断开状态！如果在线程等待期间栅栏断开或重置，此方法会引发 BrokenBarrierError 错误，注意添加异常处理

    1.2 reset 重置线程栅栏数量，返回默认的空状态，即当前阻塞的线程重新来过，如果在线程等待期间栅栏断开或重置，此方法会引发 BrokenBarrierError 错误，注意添加异常处理

2. Demo

    ```python
    # src/PythonThread/010.py
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
    ```

### 八、同步队列 queue

[queue 模块实现了多生产者、多消费者队列。这特别适用于消息必须安全地在多线程间交换的线程编程。模块中的 Queue 类实现了所有所需的锁定语义。](https://docs.python.org/zh-cn/3/library/queue.html)

1. Demo

    ```python
    # src/PythonThread/011.py
    import threading
    import queue

    q = queue.Queue()

    def worker():
        while True:
            item = q.get()
            print(f'Working on {item}')
            print(f'Finished {item}')
            q.task_done()

    # Turn-on the worker thread.
    threading.Thread(target=worker, daemon=True).start()

    # Send thirty task requests to the worker.
    for item in range(30):
        q.put(item)

    # Block until all tasks are done.
    q.join()
    print('All work completed')
    ```

### 九、小结

1. 官网的Python解释器是基于C开发的，存在GIL,若您想要克服这个问题，您可以使用其他语言开发的Python解释器；或者通过多进程来尝试解决问题

2. 互斥锁 Lock 主要针对多个线程同时操作同一个数据，使用互斥锁可以保证数据正常修改或者访问

3. 事件 Event 主要用于唤醒正在阻塞等待状态的线程

4. Condition 提供了一种多线程通信机制，假如线程 1 需要数据，那么线程 1 就阻塞等待，这时线程 2 就去制造数据，线程 2 制造好数据后，通知线程 1 可以去取数据了，然后线程 1 去获取数据

5. Timer 指定时间间隔后启动线程

6. Semaphore 信号量可以通过内置计数器来控制同时运行线程的数量，启动线程(消耗信号量)内置计数器会自动减一，线程结束(释放信号量)内置计数器会自动加一；内置计数器为零，启动线程会阻塞，直到有本线程结束或者其他线程结束为止

7. Barrier 栅栏对象，多线程 Barrier 会设置一个线程栅栏数量 parties ，如果等待的线程数量没有达到栅栏数量 parties ，所有线程会处于阻塞状态，当等待的线程到达了这个数量就会唤醒所有的等待线程。
