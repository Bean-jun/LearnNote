"""
这里我会多少种就写多少了~
- 对函数的装饰
    1. 普通装饰器
    2. 可以传递参数的装饰器
    3. 带参数的装饰器
    4. 基于类实现装饰器&&可以传递参数的类装饰器
- 对类的装饰
    5. 函数装饰器对类的装饰
    6. 类装饰器对类的装饰
    7. 带参数的类的类装饰器
- 停
    不写了~,感觉在套娃，关于这部分的应用会在后面的框架中介绍
"""


# 1. 普通装饰器
def function_1(f):
    def inner():
        print("函数传递进来的是：{}".format(f))
        return f()

    return inner


@function_1
def func_1():
    print("func_1")


# 2. 可以传递参数的装饰器
def function_2(f):
    def inner(*args, **kwargs):
        print("函数传递进来的是：{}".format(f))
        return f(*args, **kwargs)

    return inner


@function_2
def func_2(name, age):
    print(f"{name}的年龄是{age}岁~")


# 3. 带参数的装饰器
def function_3(name):
    def param(f):
        def inner(*args, **kwargs):
            print(f"name的值是:{name}")
            print("函数传递进来的是：{}".format(f))
            return f(*args, **kwargs)

        return inner

    return param


@function_3("function_3")
def func_3():
    print("func_3")


# 4. 基于类实现装饰器&&可以传递参数的类装饰器
class Decorator_1():
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        if callable(self.f):
            print("函数传递进来的是：{}".format(self.f))
            return self.f(*args, **kwargs)
        raise Exception("不要瞎搞哦~")


@Decorator_1
def func_4():
    print("func_4")


@Decorator_1
def func_5(name, age):
    print(f"{name}的年龄是{age}岁~")


# 5. 函数装饰器对类的装饰
def function_5(cls):
    def inner(*args, **kwargs):
        print("类传递进来的是：{}".format(cls))
        return cls(*args, **kwargs)

    return inner


@function_5
class A():
    def __init__(self, name):
        self.name = name

    def __del__(self):
        print(self.name)


# 6. 类装饰器对类的装饰
class Decorator_2():
    def __init__(self, decorator_class):
        self.decorator_class = decorator_class

    def __call__(self, *args, **kwargs):
        print("类传递进来的是：{}".format(self.decorator_class))
        return self.decorator_class(*args, **kwargs)


@Decorator_2
class B():
    def __init__(self, name):
        self.name = name

    def __del__(self):
        print(self.name)


# 7. 带参数的类的类装饰器
class Decorator_3():
    def __init__(self, param):
        self.param = param

    class Inner():
        def __init__(self, decorator_class):
            self.decorator_class = decorator_class

        def __call__(self, *args, **kwargs):
            print("我是类中的类，传进来的是：{}".format(self.decorator_class))
            return self.decorator_class(*args, **kwargs)

    def __call__(self, decorator_class):
        return self.Inner(decorator_class)

    def __del__(self):
        print("参数值为：{}".format(self.param))


@Decorator_3("--我是参数--")
class C():
    def __init__(self, name):
        self.name = name

    def __del__(self):
        print(self.name)


if __name__ == '__main__':
    func_1()
    func_2("小明", 23)
    func_3()
    func_4()
    func_5("小明", 23)
    a = A("小明")
    b = B("小红")
    c = C("小黑")
