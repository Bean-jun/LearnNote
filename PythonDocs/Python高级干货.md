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

 好了，别说了，看看吧，你刚刚那个function(func)()()不嫌恶心？直奔主题~什么是装饰器？有啥用~有多少中写法~

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

什么？？？？func()()还不够简单？？？看这个

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
