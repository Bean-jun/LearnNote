def function(args):
    def inner():
        print("function函数传递进来的是：{}".format(args))
        return args

    return inner


def func():
    print("我是func函数哦~")


if __name__ == '__main__':
    # 先传字符串进去
    function("哈哈哈")()  # function函数传递进来的是：哈哈哈
    # 传个被执行了的函数进去
    function(func())()  # function函数传递进来的是：None     这里解释下func函数返回值是None
    # 传个函数名进去
    function(func)()  # function函数传递进来的是：<function func at 0x100f6b430>
    # 好家伙，上面那个是什么鬼，难不成可以再一次调用？？？？我们试试嘛~
    function(func)()()  # function函数传递进来的是：<function func at 0x105dd5430>   我是func函数哦~
