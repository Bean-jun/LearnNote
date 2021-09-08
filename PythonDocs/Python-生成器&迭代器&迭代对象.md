### 一、可迭代对象

​        实现了能返回迭代器的 iter 方法，或者实现了 getitem 方法而且其参数是从零开始的索引，就可以称之为可迭代对象。

```python
# PythonDocs/src/024.py

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
    print(isinstance(MyIter, Iterator))  # False, 这里没有实现__next__方法, 故不是
    # 查看输出效果
    for i in MyIter:
        print(i)
```



### 二、迭代器

​        迭代器要实现__next__和__iter__两个方法，__next__用于获取下一个元素，__iter__方法用于迭代器本身，因此迭代器可以迭代，但是可迭代对象不是迭代器。

```python
# PythonDocs/src/025.py

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
```



### 三、生成器

​		生成器是一个特殊的迭代器，可以被用作控制循环的迭代行为，使用yield返回值函数，每次调用yield会暂停，而可以使用next()函数和send()函数恢复生成器。

```python
# PythonDocs/src/026.py

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
```

​		关于yield后面会进一步说明



### 四、小结

​		生成器是特殊的Iterator对象，但list、dict、str虽然是Iterable（可迭代对象），却不是Iterator（迭代器）。
​		

