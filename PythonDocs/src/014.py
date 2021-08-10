def function(args):
    def inner():
        print("function函数传递进来的是：{}".format(args))
        return args()

    return inner


@function
def func_1():
    print("我是func_1函数哦~")


def func_2():
    print("我是func_2函数哦~")


if __name__ == '__main__':
    """
    下面两种结果是一样的，原因就在于@function放在函数func_1上面其实就是相当于变成了这样
    func_1 = function(func_1)
    那么在执行func_1()时，其实就是在执行function(func_1)()咯~
    """
    func_1()
    function(func_2)()
