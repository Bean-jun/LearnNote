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

3. 进阶点玩法咯

   ```python
   # PythonDocs/src/016.py
   
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
   ```

4. 看看property装饰器咯~

   方法2好像可以，但是看着好憋扭哦~，怎么办？？   哈哈哈哈，看
   
   ```python
   # PythonDocs/src/017.py
   
   class People():
       def __init__(self, name, age):
           self.__name = name
           self.__age = age
   
       def name(self):
           return self.__name
   
       def age(self):
           return self.__age
   
   
   if __name__ == '__main__':
       people = People("小明", 23)
       try:
           print(f"{people.__name}的年龄是{people.__age}")
       except Exception as e:
           print(e.args)
       # 哦豁~，好像没法正常访问哎~那我们怎么办呢
       # 1. 直接访问 对于私有属性可以使用    对象._类名__属性  不推荐
       print(f"{people._People__name}的年龄是{people._People__age}")
       # 2. 定义方法去访问
       print(f"{people.name()}的年龄是{people.age()}")
   ```
   
   方法2好像可以，但是看着好憋扭哦 ~ ，怎么办？？   哈哈哈哈，看~
   
   ```python
   # PythonDocs/src/018.py
   
   class People():
       def __init__(self, name, age):
           self.__name = name
           self.__age = age
   
       @property
       def name(self):
           return self.__name
   
       @property
       def age(self):
           return self.__age
   
   
   if __name__ == '__main__':
       people = People("小明", 23)
       # 简单多了吧
       print(f"{people.name}的年龄是{people.age}")
   ```
   
   看看property的高级玩法 ~ 
   
   注意上面的我们可以直接使用了，那么可以设置值嘛 ~ 你可以试试，不行哦 ~  怎么办，我们以年龄为例，看~
   
   ```python
   # PythonDocs/src/019.py
   
   class People():
       def __init__(self, name, age):
           self.name = name
           self.__age = age
   
       @property
       def age(self):
           # 读取属性
           return self.__age
   
       @age.setter
       def age(self, val):
           # 设置属性
           self.__age = val
   
       @age.deleter
       def age(self):
           # 删除属性
           del self.__age
   
   
   if __name__ == '__main__':
       people = People("小明", 23)
       # 简单多了吧
       people.age += 1
       print(f"{people.name}的年龄是{people.age}")
   ```
   
   不过还有一种写法，可以看看，都差不多~
   
   ```python
   # PythonDocs/src/020.py
   
   class People():
       def __init__(self, name, age):
           self.name = name
           self.__age = age
   
       def get_age(self):
           # 读取属性
           return self.__age
   
       def set_age(self, val):
           # 设置属性
           self.__age = val
   
       def del_age(self):
           # 删除属性
           del self.__age
   
       age = property(get_age, set_age, del_age)
   
   
   if __name__ == '__main__':
       people = People("小明", 23)
       # 简单多了吧
       people.age += 1
       print(f"{people.name}的年龄是{people.age}")
   ```
   
   

