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