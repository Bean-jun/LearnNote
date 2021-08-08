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