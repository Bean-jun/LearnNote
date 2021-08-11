"""
1. 多层级装饰器如何理解~
    从下往上包装，从上往下执行

2. 装饰器在使用时有什么需要注意的嘛~
    在你写@时就注定这段代码不再平凡，在你执行之前，Python解释器会主动将装饰效果先装饰完成，方便你后期直接执行，
    这部分在很多新手在使用时，他们将装饰器函数或者类装饰之后，进行程序调试时感觉很奇怪，明明没有调用被装饰的函数，
    但是装饰器函数却被执行了

3. 当前存在的问题:
    被修饰的函数名称会发生改变哦~
    使用functools中的wraps修复即可
"""


def decorator_1(f):
    print("我是1号装饰器，现在在外部工作环境中~")

    def inner(*args, **kwargs):
        print("我是1号装饰器，现在在内部工作环境中~")
        return f(*args, **kwargs)

    return inner


def decorator_2(f):
    print("我是2号装饰器，现在在外部工作环境中~")

    def inner(*args, **kwargs):
        print("我是2号装饰器，现在在内部工作环境中~")
        return f(*args, **kwargs)

    return inner


@decorator_1
@decorator_2
def func_1():
    print("~~~~~~我是func_1函数哦~~~~")


def func_2():
    print("~~~~~~我是func_2函数哦~~~~")


@decorator_2
def func_3():
    print("~~~~~~我是func_3函数哦~~~~")


def func_4():
    print("~~~~~~我是func_4函数哦~~~~")


from functools import wraps


def decorator_3(f):
    print("我是3号装饰器，现在在外部工作环境中~")

    @wraps(f)
    def inner(*args, **kwargs):
        print("我是3号装饰器，现在在内部工作环境中~")
        return f(*args, **kwargs)

    return inner


@decorator_3
def func_5():
    print("~~~~~~我是func_5函数哦~~~~")


if __name__ == "__main__":
    func_1()
    # 本质上和第一种没区别的
    decorator_1(decorator_2(func_2))()

    # 看看这个
    print("当前被执行函数名称：", func_3.__name__)  # 当前被执行函数名称： inner
    print("当前被执行函数名称：", func_4.__name__)  # 当前被执行函数名称： func_4
    # 遇到这样的情况咱们怎么办?名字被改了~ 请看func_6函数及改造过的装饰器~
    print("当前被执行函数名称：", func_5.__name__)  # 当前被执行函数名称： func_5
    # 哦豁~ 使用functools中的wraps修复即可
