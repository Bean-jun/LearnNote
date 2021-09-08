from collections import Iterable, Iterator  # 可迭代对象, 迭代器


def gen(num):
    yield num + 1
    yield num + 2
    yield num + 3
    yield num + 4


if __name__ == '__main__':
    print(isinstance(gen(10), Iterable))
    print(isinstance(gen(10), Iterator))
    for i in gen(10):
        print(i)
