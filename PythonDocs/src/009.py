# 先定义一个函数
def function():
    print("我是function函数哦~")

    # 然后再定义一个函数
    def inner():
        print("我是inner函数哦~")

    # 好了, 这会我们的function函数有一个返回值
    return inner


if __name__ == '__main__':
    # 先调用函数看看结果及返回值嘛
    f = function()  # 我是function函数哦~
    print(f)  # <function function.<locals>.inner at 0x104795430>
    # 好家伙，上面的结果看懵了不是，说是返回了函数？？？ 我们借助callable查看是否可以调用
    print("当前内容是否是可以调用对象：{}".format(callable(f)))  # 当前内容是否是可以调用对象：True
    # 歪？？？ 那就试试呗, 对了，别被迷糊了哦~
    f()  # 我是inner函数哦~
    # 那么想要一次性直接执行到内部咋办呢？真心的感觉好恶心哦~
    function()()
