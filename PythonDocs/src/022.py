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
