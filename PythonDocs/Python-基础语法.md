1. 查看Python版本

   ```shell
   python3 --version
   ```

2. 第一个HelloWord程序

   ```python
   # PythonDocs/src/001.py
   
   print("Hello, Word")
   ```

3. 变量赋值

   ```python
   # PythonDocs/src/002.py
   
   # 单个变量赋值
   name = "小明"
   print(name)
   
   # 多变量赋统一值
   tom_age = jerry_age = 10
   print(f"tom的年龄为{tom_age}, jerry的年龄为{jerry_age}")
   
   # 多个变量赋不同值
   name, age = "小明", 23
   print(f"{name}的年龄是{age}岁")
   ```

4. 运算符

   ```python
   # PythonDocs/src/003.py
   
   # 算术运算符
   """
   +	加 - 两个对象相加	 
   -	减 - 得到负数或是一个数减去另一个数	 
   *	乘 - 两个数相乘或是返回一个被重复若干次的字符串 
   /	除 - x 除以 y	 
   %	取模 - 返回除法的余数	 
   **	幂 - 返回x的y次幂	
   //	取整除 - 向下取接近商的整数
   """
   
   # 比较运算
   """
   ==	等于 - 比较对象是否相等 
   !=	不等于 - 比较两个对象是否不相等	 
   >	大于 - 返回x是否大于y 
   <	小于 - 返回x是否小于y。所有比较运算符返回1表示真，返回0表示假。 
   >=	大于等于 - 返回x是否大于等于y。	 
   <=	小于等于 - 返回x是否小于等于y。
   """
   
   # 位运算
   """
   &	按位与运算符：参与运算的两个值,如果两个相应位都为1,则该位的结果为1,否则为0 
   |	按位或运算符：只要对应的二个二进位有一个为1时，结果位就为1。 
   ^	按位异或运算符：当两对应的二进位相异时，结果为1 
   ~	按位取反运算符：对数据的每个二进制位取反,即把1变为0,把0变为1。~x 类似于 -x-1  
   <<	左移动运算符：运算数的各二进位全部左移若干位，由"<<"右边的数指定移动的位数，高位丢弃，低位补0。 
   >>	右移动运算符：把">>"左边的运算数的各二进位全部右移若干位，">>"右边的数指定移动的位数 
   """
   
   # 逻辑运算
   """
   and	x and y	布尔"与" - 如果 x 为 False，x and y 返回 x 的值，否则返回 y 的计算值。	 
   or	x or y	布尔"或" - 如果 x 是 True，它返回 x 的值，否则它返回 y 的计算值。	 
   not	not x	布尔"非" - 如果 x 为 True，返回 False 。如果 x 为 False，它返回 True。 
   """
   
   # 成员运算
   """
   in	如果在指定的序列中找到值返回 True，否则返回 False。	 
   not in	如果在指定的序列中没有找到值返回 True，否则返回 False。
   """
   
   # 身份运算符
   """
   is	 判断两个标识符是不是引用自一个对象 
   is not	 判断两个标识符是不是引用自不同对象
   
   is 与 == 区别：
       is 用于判断两个变量引用对象是否为同一个， == 用于判断引用变量的值是否相等。
   """
   ```

5. 条件语句

   ```python
   # PythonDocs/src/004.py
   
   a = 20
   b = 10
   
   # if结构
   if a > b:
       print("yes")
   
   # if...else结构
   if a > b:
       print("yes")
   else:
       print("no")
   
   # if...elif结构
   if a > b:
       print("yes")
   elif b > 0:
       print("???")
   else:
       print("no")
   
   # 嵌套分支
   if a > b:
       if a > 21:
           print("yes")
       elif b > 0:
           print("???")
   else:
       print("no")
   ```

6. 循环语句

   ```python
   # PythonDocs/src/005.py
   
   # for循环
   for i in range(10):
       print(i)
   
   # while循环
   flag = True
   a = 0
   while True:
       if flag is False:
           break
       a += 1
       print('哈' * a, "!")
       if a > 6:
           flag = False
   ```

7. 函数

   ```python
   # PythonDocs/src/006.py
   
   # 无参函数
   def function_1():
       print("这是一个函数")
       
   function_1()
   
   # 有参函数
   def function_2(name):
       print(f"大家好，我叫{name}")
       
   function_2("小明")
   
   # 通用参数函数
   def function_3(*args, **kwargs):
       print("元组形式:", args)
       print("字典形式:", kwargs)
       
   function_3(1, 2, 3, 4, name="小明", age=23)
   ```

8. 面向对象-01

   ```python
   # PythonDocs/src/007.py
   
   class Foo():
       def __init__(self, msg):
           self.msg = msg
   
       def show(self):
           print(self.msg)
   
       @classmethod
       def foo_class_method(cls):
           print(f"我是{cls.__name__}类, 但是我在调用自己的静态方法哦~  ", end='')
           cls.foo_static_method()
   
       @staticmethod
       def foo_static_method():
           print("Foo的静态方法")
   
   
   if __name__ == '__main__':
       foo = Foo("哈哈哈")
       foo.show()
       foo.foo_class_method()
       foo.foo_static_method()
   ```

9. 面向对象-02

   ```python
   # PythonDocs/src/008.py
   
   class A():
   
       def __init__(self):
           pass
   
       def run(self):
           raise Exception("请子类实现")
   
   class B(A):
   
       def __init__(self, name):
           super().__init__()
           self.name = name
   
       def run(self):
           print(f"我{self.name}是被迫实现的run方法哦~")
   
   
   if __name__ == '__main__':
       b = B("小明")
       b.run()
   ```

10. 面向对象-03 多继承

    理解下方两段code

    ```python
    class A():
        def say(self):
            print("A say")
    class B(A):
        pass
    class C():
        def say(self):
            print("C say")
    class D(B, C):
        pass

    d=D()
    d.say()
    print(D.__mro__)
    ```
    
    ```python
    class A():
        def say(self):
            print("A say")
    class B(A):
        pass
    class C(A):
        def say(self):
            print("C say")
    class D(B, C):
        pass

    d=D()
    d.say()
    print(D.__mro__)
    ```

