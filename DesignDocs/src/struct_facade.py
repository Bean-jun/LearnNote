# 外观模式
from abc import ABCMeta, abstractmethod

class Component(metaclass=ABCMeta):
    # 通用零部件

    @abstractmethod
    def __init__(slef):
        # 初始化
        pass

    @abstractmethod
    def boot(self):
        # 启动
        pass

    @abstractmethod
    def stop(self):
        # 停止
        pass


class Engine(Component):

    def __init__(self):
        self.name = "本田发动机"

    def boot(self):
        print(f"{self.name} 启动中")

    def stop(self):
        print(f"{self.name} 已停止")
    

class Electrical(Component):

    def __init__(self):
        self.name = "汽车电器件"

    def boot(self):
        print(f"{self.name} 启动中")

    def stop(self):
        print(f"{self.name} 已停止")


class Display(Component):

    def __init__(self):
        self.name = "汽车中控显示器"

    def boot(self):
        print(f"{self.name} 启动中")

    def stop(self):
        print(f"{self.name} 已停止")
    

class UserOperator:

    def __init__(self):
        self.engine = Engine()
        self.electrical = Electrical()
        self.display = Display()

    def start(self):
        self.engine.boot()
        self.electrical.boot()
        self.display.boot()
    
    def stop(self):
        self.display.stop()
        self.electrical.stop()
        self.engine.stop()
    
    def stop_display(self):
        self.display.stop()
    

if __name__ == "__main__":
    op = UserOperator()
    op.start()  # 点火
    op.stop_display() # 关闭中控显示器
    # 小车行驶.....
    op.stop() #熄火