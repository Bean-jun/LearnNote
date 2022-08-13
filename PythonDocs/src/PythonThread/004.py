import threading

lock = threading.Lock()

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
