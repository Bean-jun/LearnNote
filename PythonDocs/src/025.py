from collections import Iterable, Iterator  # 可迭代对象, 迭代器


class MyIterator():
    def __init__(self, num):
        self.a = 1
        self.b = 1
        self.c = self.a + self.b
        self.num = num

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            if self.num >= 2:
                self.c = self.a + self.b
                self.a = self.b
                self.b = self.c
                self.num -= 1
                return self.c
            else:
                raise StopIteration


if __name__ == '__main__':
    MyIter = MyIterator(4)
    # 判断是否为可迭代对象
    print(isinstance(MyIter, Iterable))  # True
    # 判断是否为迭代器
    print(isinstance(MyIter, Iterator))  # True
    # 查看输出效果
    for i in MyIter:
        print(i)
