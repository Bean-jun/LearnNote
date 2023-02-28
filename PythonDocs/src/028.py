"""
                            循环队列（时间分片）
    ------------------------------------------------------------------
--->|    |    |    |    |    |    |    |    |    |    |    |    |    |---->
|   ------------------------------------------------------------------    |
|                                                                         |
<--------------------------------------------------------------------------
"""
import datetime
import time
import copy
import threading


class SimpleWindow:

    def __init__(self, max_size=60, interval=None, log=False):
        self.max_size = max_size
        self.left = 0
        self.right = 0
        self.queue = [0 for _ in range(self.max_size)]
        self.frequency = 0
        self.start = False
        self.interval = 60 / self.max_size if not interval else interval
        self.log = log

    # 获取当前限流时间段内请求次数
    def size(self):
        if self.left <= self.right:
            self.frequency = sum(self.queue[self.left: self.right])
        else:
            self.frequency = sum(self.queue[0: self.right]) +\
                sum(self.queue[self.left: self.max_size])
        return self.frequency

    # 当用户请求时，+1
    def incr(self):
        if not self.start:
            loop = threading.Thread(target=self._loop, name="window_loop")
            loop.daemon = True
            loop.start()

        # 在当前右侧窗口 +1
        self.queue[self.right] += 1

    # 启动窗口事件 实时计算当前窗口中
    def _loop(self):
        self.start = True
        flag = False
        while True:
            if self.log:
                self._print()
            # 达到最大临界点，左侧开始随着右侧进行滑动
            if self.right + 1 >= self.max_size:
                flag = True
            self.right = (self.right + self.max_size + 1) % self.max_size
            if flag:
                # 左侧窗口进行滑动，同时左侧窗口滑动之前恢复原先窗口值为0
                self.queue[self.left] = 0
                self.left = (self.left + self.max_size + 1) % self.max_size
            time.sleep(self.interval)

    def _print(self):
        _queue = copy.deepcopy(self.queue)
        _queue[self.left] = "L"
        _queue[self.right] = "R"
        print("----sub thread----", self.left, self.right)
        # print("----sub thread----", _queue, self.left, self.right)


def main():
    max_req = 10  # 1分钟内最大X次
    success_nums = 0
    w = SimpleWindow(600, log=False)  # 1分钟分成Y份
    for _ in range(10000000):
        if w.size() > max_req:
            success_nums = 0
            print(datetime.datetime.now(), "睡", w.size())
            time.sleep(5)
            continue
        w.incr()
        success_nums += 1
        print(datetime.datetime.now(), "请求成功%s次" % success_nums, w.size())
        # time.sleep(0.000001)
        time.sleep(4)


if __name__ == "__main__":
    main()
