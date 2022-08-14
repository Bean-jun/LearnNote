import multiprocessing
import os


class ProcessChild(multiprocessing.Process):

    def __init__(self, group=None, target=None, name=None, args=()):
        super().__init__(group=group, target=target, name=name, args=args)

    def run(self):
        print("当前获取数字：", self._args, "当前获取进程ID: ", os.getpid())


def main():
    tasks = []
    for i in range(10):
        tasks.append(ProcessChild(args=(i, )))

    [i.start() for i in tasks]

    [i.join() for i in tasks]

    print("进程结束")


if __name__ == "__main__":
    main()
    # 当前获取数字： (2,) 当前获取进程ID:  39532
    # 当前获取数字： (1,) 当前获取进程ID:  39531
    # 当前获取数字： (4,) 当前获取进程ID:  39534
    # 当前获取数字： (7,) 当前获取进程ID:  39537
    # 当前获取数字： (6,) 当前获取进程ID:  39536
    # 当前获取数字： (9,) 当前获取进程ID:  39539
    # 当前获取数字： (0,) 当前获取进程ID:  39530
    # 当前获取数字： (8,) 当前获取进程ID:  39538
    # 当前获取数字： (5,) 当前获取进程ID:  39535
    # 当前获取数字： (3,) 当前获取进程ID:  39533
    # 进程结束
