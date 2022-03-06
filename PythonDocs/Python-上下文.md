### 一、简介

1. 看看定义 ~

   看啥哦 ~ ，看啥哦，先看段代码，你一定熟悉 ~ 

   ```python
   # PythonDocs/src/021.py
   
   with open('log.txt', 'r', encoding='utf-8') as f:
       data = f.read()
   
   print(data)
   ```

   这个`with`看起来很奇怪哦，事实上对一个文件的操作也可以这个样~

   ```python
   # PythonDocs/src/021.py
   
   fObj = open('log.txt', 'r', encoding='utf-8')
   data_content = fObj.read()
   fObj.close()
   print(data_content)
   ```

   怎么看上面的方案都更优雅~

2. 自定义上下文

   官方说，在内部实现`__enter__`及`__exit__`方法即可哦，那我们看下如何实现~

   ```python
   # PythonDocs/src/022.py
   
   class Foo():
       def run(self):
           print(f"我是{self}")
   
       def __enter__(self):
           print(f"{self}被打开了~")
           return self
   
       def __exit__(self, exc_type, exc_val, exc_tb):
           print(f"{self}被关闭了~")
   
   
   if __name__ == '__main__':
       with Foo() as obj:
           obj.run()
           
   # 以下是我们的结果哦~   
   
   # <__main__.Foo object at 0x1025d5a60>被打开了~
   # 我是<__main__.Foo object at 0x1025d5a60>
   # <__main__.Foo object at 0x1025d5a60>被关闭了~
   ```

   看起来好像是先调用了`__enter__`方法，然后去执行我们的自定义内容，最后执行`__exit__`方法内的内容，一般对于有关联的两件事情，我们可以使用上下文让他们链接，避免操作上的失误哦~

3. 还有没有别的写法？

   还真有，面试被问到，书上看到过，忘记了，emmmm，写一个~

   ```python
   # PythonDocs/src/023.py
   
   from contextlib import contextmanager
   
   
   @contextmanager
   def func():
       print("我又开始了~")
       try:
           yield 1
       finally:
           print("完事了~, 看")
   
   
   if __name__ == '__main__':
       with func() as f:
           print(f)
   ```

   要是留心思看下源码，你就会发现，这个玩意还是丢到`__enter__`及`__exit__`里面去了~

   ```python
   # 源码内容，大家可以自己看下哦~
   
   def contextmanager(func):
       @wraps(func)
       def helper(*args, **kwds):
           return _GeneratorContextManager(func, args, kwds)
       return helper
     
   class _GeneratorContextManager(_GeneratorContextManagerBase,
                                  AbstractContextManager,
                                  ContextDecorator):
       def _recreate_cm(self):
           return self.__class__(self.func, self.args, self.kwds)
   
       def __enter__(self):
           del self.args, self.kwds, self.func
           try:
               return next(self.gen)
           except StopIteration:
               raise RuntimeError("generator didn't yield") from None
   
       def __exit__(self, type, value, traceback):
           if type is None:
               try:
                   next(self.gen)
               except StopIteration:
                   return False
               else:
                   raise RuntimeError("generator didn't stop")
           else:
               if value is None:
                   value = type()
               try:
                   self.gen.throw(type, value, traceback)
               except StopIteration as exc:
                   return exc is not value
               except RuntimeError as exc:
                   if exc is value:
                       return False
                   if type is StopIteration and exc.__cause__ is value:
                       return False
                   raise
               except:
                   if sys.exc_info()[1] is value:
                       return False
                   raise
               raise RuntimeError("generator didn't stop after throw()")
   ```


### 二、应用

1. 举个🌰，咱们在使用flask框架编写web应用时，多数小伙伴会选择flask-sqlalchemy这个插件实现对数据库的操作，很多小伙伴尝尝会写出这样的代码(:)偷笑)

   ```python
   user = User(.....)
   db.session.add(user)
   try:
       db.session.commit()
   except:
       db.session.rollback()
   ```
   
   当然啦，酱紫写是没有任何毛病滴，可是每次创建一个model对象都要这样吼累哦，不是嘛？
   
   于是有了这样的写法 :)
   
   ```python
   def db_session_commit():
       try:
           db.session.commit()
           return True
       except:
           db.session.rollback()
           return False
   
   user = User(....)
   db.session.add(user)
   db_session_commit()	# 可以多次复用，倒也是省事了不少
   ```
   
   那么还有没有其他的方案呢？当然有来，看看这个
   
   ```python
   from contextlib import contextmanager
   from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
   
   
   class SQLAlchemy(_SQLAlchemy):
   
       @contextmanager
       def auto_save(self):
           try:
               yield
               self.session.commit()
           except:
               self.session.rollback()
   
   user = User(....)
   with db.auto_save():
       db.session.add(user)
   ```
   
   看起来好像高大上了不少哦~ 哦嚯嚯嚯