def function():
    n = 10

    def inner():
        nonlocal n
        print("n的值是：{} , 对应内存地址为{}".format(n, id(n)))

    return inner


if __name__ == '__main__':
    function()()
