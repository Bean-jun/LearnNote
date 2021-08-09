def function(args):
    def inner():
        print("function函数传递进来的是：{}".format(args))
        return args()

    return inner


@function
def func():
    print("我是func函数哦~")


if __name__ == '__main__':
    func()
