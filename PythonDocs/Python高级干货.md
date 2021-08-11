### 一、闭包

1. 初识闭包代码

   啥也不说，先看看代码哦~

    ```python
    # PythonDocs/src/009.py
    
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
    ```

2. 进一步了解

   我们尝试往里面传递一些参数试试嘛~

    ```python
    # PythonDocs/src/010.py
    
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
    ```


3. 再进一步

   这会我想尝试在内部函数中调用外层函数的变量，甚至我还想修改它~

    ```python
    # PythonDocs/src/011.py
    
    def function():
        n = 10
        
        def inner():
            nonlocal n
            # 这里要尤为注意，内部函数不可以直接修改外部函数的值[不可变]，否则会抛出异常，若是必须修改请加上nonlocal声明
            n += 1
            print("n的值是：{} , 对应内存地址为{}".format(n, id(n)))
        
        return inner
    
    
    if __name__ == '__main__':
        function()()
    ```

### 二、装饰器

 好了，别说了，看看吧，你刚刚那个`function(func)()()`不嫌恶心？直奔主题 ~ 什么是装饰器？有啥用 ~ 有多少中写法~

 哈哈哈哈，那么接下来就聊聊简化方式嘛，先看个demo

```python
# PythonDocs/src/012.py

def function(args):
    def inner():
        print("function函数传递进来的是：{}".format(args))
        return args

    return inner


@function
def func():
    print("我是func函数哦~")


if __name__ == '__main__':
    func()()  # function函数传递进来的是：<function func at 0x105dd5430>   我是func函数哦~
```

什么？？？？`func()()`还不够简单？？？看这个

```python
# PythonDocs/src/013.py

def function(args):
    def inner():
        print("function函数传递进来的是：{}".format(args))
        return args()

    return inner


@function
def func():
    print("我是func函数哦~")


if __name__ == '__main__':
    func()  # function函数传递进来的是：<function func at 0x105dd5430>   我是func函数哦~
```

1. 什么是装饰器？

   个人理解哈~  就是在不修改原函数的情况下添加更多的功能~ 上面的两个小栗子就是装饰器的应用，在不修改`func`函数的情况下添加一点点功能~

   说到这里大家就不乐意了，这`@function`是什么鬼捏~。好的，那么我们来看下这个写法~

   ```python
   # PythonDocs/src/014.py
   
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
   ```

2. 装饰器的多种写法~

   没错，之前面试被问到了，问我怎么实现，我说就上面这种哇~~

   结果可想而知，凉凉~

   下面就来看看咯~

   ```python
   # PythonDocs/src/015.py
   
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
   ```

   
