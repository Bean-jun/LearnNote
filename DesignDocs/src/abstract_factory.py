from abc import ABCMeta, abstractmethod


class ConnectError(Exception):
    pass


class ConnectFactory(metaclass=ABCMeta):

    @abstractmethod
    def connect(self):
        raise


class MySQLCommunityConnect(ConnectFactory):

    def connect(self):
        return "MySQL社区版连接obj"


class MySQLEnterpriseConnect(ConnectFactory):

    def connect(self):
        return "MySQL企业版连接obj"


class PgSQLCommunityConnect(ConnectFactory):

    def connect(self):
        return "PgSQL社区版连接obj"


class PgSQLEnterpriseConnect(ConnectFactory):

    def connect(self):
        return "PgSQL企业版连接obj"


class SQLServerCommunityConnect(ConnectFactory):

    def connect(self):
        return "SQLServer社区版连接obj"


class SQLServerEnterpriseConnect(ConnectFactory):

    def connect(self):
        return "SQLServer企业版连接obj"


def connect_community_factory(db_type):

    if db_type == "MySQL":
        return MySQLCommunityConnect()
    if db_type == "PgSQL":
        return SQLServerCommunityConnect()
    if db_type == "SQLServer":
        return SQLServerCommunityConnect()

    raise ConnectError("数据库连接异常")


def connect_enterprise_factory(db_type):

    if db_type == "MySQL":
        return MySQLEnterpriseConnect()
    if db_type == "PgSQL":
        return SQLServerEnterpriseConnect()
    if db_type == "SQLServer":
        return SQLServerEnterpriseConnect()

    raise ConnectError("数据库连接异常")


# 抽象工厂集合
def connect_factory(price, db_type):
    if price > 0:
        return connect_enterprise_factory(db_type)
    return connect_community_factory(db_type)


if __name__ == "__main__":
    # 通过预算，我们给这个客户端分配不同的数据库服务器
    conn = connect_factory(0, "MySQL")
    print(conn.connect())
    conn = connect_factory(100, "PgSQL")
    print(conn.connect())
    conn = connect_factory(0, "SQLServer")
    print(conn.connect())
