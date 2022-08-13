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
