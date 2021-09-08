from collections import Iterable, Iterator  # 可迭代对象, 迭代器


class MyIterable():
    def __init__(self, *args):
        self.args = args

    def __iter__(self):
        return iter(self.args)


if __name__ == '__main__':
    MyIter = MyIterable(12, 23, 1)
    # 判断是否为可迭代对象
    print(isinstance(MyIter, Iterable))  # True
    # 判断是否为迭代器
    print(isinstance(MyIter, Iterator))  # False
    # 查看输出效果
    for i in MyIter:
        print(i)
