### 一、啥是元类

​		有些同学看到这个就傻眼了，啥东西，没啥概念哦~ 

​		事实上确实如此，笔者也是云里雾里学完django、flask几个框架并实际使用到应用中之后才回过头来思考这个问题的（主要是这些框架源码看不太懂）！好了言归正传，那么什么是元类呢？

​		元类是制造类的工厂，这是`流程的Python`中的原话，简单来说就是我们一般使用`class`创建的类对象中的类是由元类创建的！！！ 好家伙，真绕啊（ps:个人理解就是创建的类的模具）。而我们常用的`type`在这里起着至关重要的作用！！！ 看栗子🌰

```python
class User():
    def __init__(self, name):
        self.name = name

user = User("张三")

print(type(user))	# <class '__main__.User'>
print(isinstance(user, User))	# True
print(type(User))	# <class 'type'>
print(isinstance(User, type))	# True
```

​		上述的栗子表明，`user`是`User`这个类的对象，那么`User`呢？何尝又不是`type`的对象呢。事实上关于`type`还有一种用法----**创建类**



### 二、使用type创建类

先看源码

```python
def __init__(self):
    pass

def __call__(self, *args, **kwargs):
    print(args, kwargs, self.var)

B = type("B", (), {"__init__": __init__, "__call__": __call__, "var": 1000})

if __name__ == '__main__':
    b = B()
    b()
```

上述代码的写法和这个是等效的

```python
class B():
    var = 100

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        print(args, kwargs, self.var)
```



### 三、抛出问题：再问何为元类？如何元编程？

其实我们已经知道了，`type`其实就是一个元类，那么问题来了，既然我们有了元类，怎么元编程？

我们知道了`type`就是元类，但是又不可以修改它的代码，那么我们就可以通过继承创建属于我们自己的元类（自己的模具），看代码：

```python
class A(type):
  
    def __init__(self, name, bases, dicts):
        super().__init__(name, bases, dicts)

    def __new__(cls, *args, **kwargs):
        return type.__new__(cls, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        print(args, kwargs, cls.var, cls)
        obj = cls.__new__(cls)
        cls.__init__(cls, *args, **kwargs)
        return obj


# 不在使用type创建类，改用A创建B类
def __init__(self):
    pass


def __call__(self, *args, **kwargs):
    print(args, kwargs, self.var)


B = A("B", (), {"__init__": __init__, "__call__": __call__, "var": 10000})
```

在上述代码中，我们将`A`继承`type`,这样就变成了一个元类，或者说超类，其实我更愿意将其理解为这样的一个内容：

​		type可以创建类，可以理解为一个模具，在上述例子中，通过A也可以创建一个类，其实可以换种思维理解为A也是一个模具，但是在使用过程中，还是找type这个模具帮忙了，需要做一些细活，最终完成一个类的创建。



**注意点** :

​		其实到现在很多同学没有注意到事情的验证性，若是有同学使用`B`来初始化一个实例就会发现，我们的这个类将会调用`A`这个元类的`__call__`方法。这个时候就会有同学问了，这是为啥？事实上要是有同学仔细调试程序就会发现，这里的`B`这个类对象其实是`A`的对象，当其调用B()开始初始化的时候就会调用类的`__call__`方法（ps:对象加()就会调用类的`__call__`方法，这是基础哦~ ）完成对`B`类对象的初始化工作。



### 四、有问有简化写法？

别说，还真就有哦，使用`metaclass`即可，效果和上面的一致，看源码

```python
class A(type):
  
    def __init__(self, name, bases, dicts):
        super().__init__(name, bases, dicts)

    def __new__(cls, *args, **kwargs):
        return type.__new__(cls, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        print(args, kwargs, cls.var, cls)
        obj = cls.__new__(cls)
        cls.__init__(cls, *args, **kwargs)
        return obj


class C(metaclass=A):
    var = 2000

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        print(args, kwargs, self.var)

```



### 五、小结

​		一般的，在创建类时，首先走的是`__new__` --> `__init__`在上述的例子中我们可以看到，在我们实例化一个普通类之前，我们的元类会先创建一个类，没错，就是一个类，在创建过程中，将会执行元类的`__new__`方法，然后执行元类的`__init__`方法以此来创建一个对象，也就是我们说的类，当这个类开始实例化时，我们会调用元类的`__call__`方法，原因就在这里`print(type(B))`结果为`# <class '__main__.A'>`，说明其实我们这里的B目前还只是A的一个对象，完全可以调用A的`__call__`方法，在这个`__call__`方法中，我们得到的cls参数就变成了B这个类，由此分别调用B类的`__new__`方法和`__init__`方法，实现实例化。

​		所以实例化对象过程的顺序：

​    	元类`__new__`方法 --> 元类`__init__`方法 --> 元类`__call__`方法 --> 普通类`__new__`方法 --> 普通类`__init__`方法



### 六、应用场景

​		django的orm，wtf-forms等等。



### 七、demo

模拟django-orm尝试demo

```python
# PythonDocs/src/PythonMetaClass/fields.py

class Field():

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return "{} type is {}".format(self.name, self.column_type)


class IntField(Field):

    def __init__(self, name):
        super(IntField, self).__init__(name, "int")


class StringField(Field):

    def __init__(self, name):
        super(StringField, self).__init__(name, "varchar(250)")
```

```python
# PythonDocs/src/PythonMetaClass/orm.py

from .fields import Field, IntField, StringField


class Orm(type):

    def __init__(self, names, bases, dicts):
        super().__init__(names, bases, dicts)

    @staticmethod
    def __new__(cls, names, bases, dicts):
        if names != "Model":
            mapping = {}
            for dic_k, dic_v in dicts.items():
                if isinstance(dic_v, Field):
                    mapping[dic_k] = dic_v

            # 剔除类属性
            for k in mapping:
                dicts.pop(k)

            dicts["__mapping__"] = mapping
            dicts["__tablename__"] = names.lower()

        return type.__new__(cls, names, bases, dicts)


class Model(dict, metaclass=Orm):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self[item]

    def save(self):
        print("save model")

        field = []
        values = []
        for _field, _values in self.__mapping__.items():
            field.append(_field)
            values.append(str(getattr(self, _field, None)))

        sql = "insert into %s (%s) values (%s);" % (self.__tablename__, ','.join(field), ','.join(values))
        print(sql)


class UserInfo(Model):
    username = StringField("username")
    age = IntField("age")


if __name__ == '__main__':
    user = UserInfo(username="张三", age=24)
    user.save()
```

