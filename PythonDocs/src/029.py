"""
                            循环队列（时间分片）
    ------------------------------------------------------------------
--->|    |    |    |    |    |    |    |    |    |    |    |    |    |---->
|   ------------------------------------------------------------------    |
|                                                                         |
<--------------------------------------------------------------------------
"""
from functools import wraps
from flask import Flask, request
import time
import copy
import threading


class Window():

    def __init__(self, max_size=60, interval=None, log=False):
        self.max_size = max_size
        self.left = 0
        self.right = 0
        self.queue = [0 for _ in range(self.max_size)]
        self._window_dict = dict()
        self.u_list = []
        self.frequency = dict()
        self.start = False
        self.interval = 60 / self.max_size if not interval else interval
        self.log = log

    # 获取当前限流时间段内请求次数
    def size(self, uid):
        if uid not in self._window_dict:
            return 0
        if self.left <= self.right:
            self.frequency[uid] = sum(
                self._window_dict[uid][self.left: self.right])
        else:
            self.frequency[uid] = sum(self._window_dict[uid][0: self.right]) +\
                sum(self._window_dict[uid][self.left: self.max_size])
        return self.frequency[uid]

    # 当用户请求时，+1
    def incr(self, uid):
        if not self.start:
            loop = threading.Thread(target=self._loop, name="window_loop")
            loop.daemon = True
            loop.start()

        # 在当前右侧窗口 +1
        if uid not in self._window_dict:
            self.u_list.append(uid)
            self._window_dict[uid] = copy.deepcopy(self.queue)
        self._window_dict[uid][self.right] += 1

    # 启动窗口事件 实时计算当前窗口中
    def _loop(self):
        self.start = True
        flag = False
        while True:
            for uid in self.u_list:
                if self.log:
                    self._print(uid)
                # 达到最大临界点，左侧开始随着右侧进行滑动
                if self.right + 1 >= self.max_size:
                    flag = True
                self.right = (self.right + self.max_size + 1) % self.max_size
                if flag:
                    # 左侧窗口进行滑动，同时左侧窗口滑动之前恢复原先窗口值为0
                    self._window_dict[uid][self.left] = 0
                    self.left = (self.left + self.max_size + 1) % self.max_size
                time.sleep(self.interval)

    def _print(self, uid):
        _queue = copy.deepcopy(self._window_dict[uid])
        _queue[self.left] = "L"
        _queue[self.right] = "R"
        print("----sub thread-uid: %s---" %
              uid, _queue,  self.left, self.right)


w = Window(60, log=True)
app = Flask(__name__)


def throttling(max_size):
    def wrapper(f):
        @wraps(f)
        def inner(*args, **kwargs):
            uid = request.args.get("uid")
            if w.size(uid) > max_size:
                return "求求您别访问了，太频繁了"
            w.incr(uid)
            return f(*args, **kwargs)
        return inner
    return wrapper


@app.get("/")
@throttling(10)
def index():
    return "index"


if __name__ == "__main__":
    app.run(port=9090, debug=True)
