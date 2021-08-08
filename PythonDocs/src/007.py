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
