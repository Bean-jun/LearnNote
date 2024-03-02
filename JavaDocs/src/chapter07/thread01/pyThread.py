import threading
import time


def func():
    time.sleep(1)
    print("run sub thread")


if __name__ == "__main__":
    t = threading.Thread(target=func, daemon=True)
    t.start()
    print("main thread")
    t.join()
