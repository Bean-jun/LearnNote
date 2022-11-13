from abc import ABCMeta, abstractmethod


class ConnectFactory(metaclass=ABCMeta):

    @abstractmethod
    def connect(self):
        raise


class MySQLEnterpriseConnect(ConnectFactory):

    def connect(self):
        return "MySQL企业版连接obj"


# 约束建造者
class Builder(metaclass=ABCMeta):

    # 帮客户购买机器
    @abstractmethod
    def buy(self):
        raise

    # 帮客户开机
    @abstractmethod
    def open(self):
        raise

    # 帮客户设置机器磁盘大小
    @abstractmethod
    def disk(self):
        raise

    # 帮客户安装数据库软件
    @abstractmethod
    def install(self):
        raise

    # 客户获取数据库实例
    @abstractmethod
    def db(self):
        raise


class BaseBuilder(Builder):

    def __init__(self):
        self._name = "客服"

    def buy(self):
        print(f"{self._name}帮助客户下单了一台数据库服务器")

    def open(self):
        print(f"{self._name}将服务器进行了开机")

    def disk(self):
        print(f"{self._name}将服务器设置为40GB")

    def install(self):
        print(f"{self._name}将数据库安装进入了服务器")

    def db(self):
        return MySQLEnterpriseConnect().connect()


class Alibuilder(BaseBuilder):

    def __init__(self):
        self._name = "阿里云客服"

    def disk(self):
        print(f"{self._name}将服务器设置为38GB")


class Huaweibuilder(BaseBuilder):

    def __init__(self):
        self._name = "华为云客服"

    def disk(self):
        print(f"{self._name}将服务器设置为39GB")


class DBDirector():
    # 数据库指挥者
    def __init__(self):
        self.builder = None

    def construct_builder(self, builder: Builder):
        self.builder = builder
        self.builder.buy()
        self.builder.open()
        self.builder.disk()
        self.builder.install()

    def db(self):
        return self.builder.db()


if __name__ == "__main__":
    # user_choice = "alibuilder"
    user_choice = "huaweibuilder"
    if user_choice == "alibuilder":
        builder = Alibuilder()
    else:
        builder = Huaweibuilder()

    # 指挥者指挥建造者进行数据库实例的构建
    instance = DBDirector()
    instance.construct_builder(builder)
    conn = instance.db()
    print("客户端获取连接对象:", conn)
