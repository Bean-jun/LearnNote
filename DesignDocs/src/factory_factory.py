from abc import ABCMeta, abstractmethod


class ConnectError(Exception):
    pass


class ConnectFactory(metaclass=ABCMeta):

    @abstractmethod
    def connect(self):
        raise


class MySQLConnect(ConnectFactory):

    def connect(self):
        return "MySQL连接obj"


class PgSQLConnect(ConnectFactory):

    def connect(self):
        return "PgSQL连接obj"


class SQLServerConnect(ConnectFactory):

    def connect(self):
        return "SQLServer连接obj"


def connect_factory(db_type):

    if db_type == "MySQL":
        return MySQLConnect()
    if db_type == "PgSQL":
        return PgSQLConnect()
    if db_type == "SQLServer":
        return SQLServerConnect()

    raise ConnectError("数据库连接异常")


if __name__ == "__main__":
    conn = connect_factory("MySQL")
    print(conn.connect())
    conn = connect_factory("PgSQL")
    print(conn.connect())
    conn = connect_factory("SQLServer")
    print(conn.connect())
    conn = connect_factory("redis")
    print(conn.connect())
