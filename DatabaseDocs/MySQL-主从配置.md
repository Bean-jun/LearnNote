# MySQL主从配置（一主一从）

### 一、环境准备

1. windows 11
2. MySQL-8.0.30

### 二、开始配置

0. 将MySQL-8.0.30分别拷贝至两个目录

    MySQL-8.0.30-winx64_master

    MySQL-8.0.30-winx64_slave

1. 编辑my.ini

    ```shell
    # 主库的my.ini文件
    #####新加入部分#######
    [mysqld]
    port=3306
    server_id=1
    log_bin=ON


    # 从库的my.ini文件
    #####新加入部分#######
    [mysqld]
    port=3307
    server_id=2
    ```

2. 编辑auto.conf（在mysql的数据文件夹下）

    ```shell
    # 修改的目的是避免uuid重复，我们保证uuid唯一就可以了

    # 主库的auto.conf
    ######新加入部分#########
    [auto]
    server-uuid=50582deb-3efc-4ee6-8a7d-4f69f1651a91
    
    
    # 从库的auto.conf
    ######新加入部分#########
    [auto]
    server-uuid=95b759aa-f4ab-489e-93e4-75f409731887

    ```

3. 创建账号

    在`主机`上创建一个账号用于从机复制使用

    ```sql
    -- 创建账号
    create user "slave"@"%" identified with mysql_native_password by "slave";

    -- 授权账号复制权限
    grant replication slave to "slave"@"%";

    -- 更新授权
    flash privileges;
    ```

4. 查询状态

    在`主机`上查询当前主节点的状态

    ```sql
    show master status;
    ```

    ```shell
    mysql> show master status;
    +-----------+----------+--------------+------------------+-------------------+
    | File      | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
    +-----------+----------+--------------+------------------+-------------------+
    | ON.000001 |     3756 |              |                  |                   |
    +-----------+----------+--------------+------------------+-------------------+
    ```

5. 设置待复制主机信息

    在`从机`上运行下面命令

    ```sql
    -- master_host 主机地址
    -- master_port 主机端口
    -- master_user 主机复制权限的用户
    -- master_password 主机复制权限的用户密码
    -- master_log_file 主机日志文件名称（见上方show master status）结果
    -- master_log_pos 主机日志文件偏移量（见上方show master status）结果
    change master to master_host='127.0.0.1',master_port=3306,master_user='slave',master_password='slave',master_log_file='ON.000001',master_log_pos=3756;
    ```

6. 开始复制

    在从机上开始复制

    ```sql
    start slave;
    ```

    查看复制信息

    ```sql
    show slave status \G;
    ```

    正常状态

    ```shell
    mysql> show slave status \G;
    *************************** 1. row ***************************
                Slave_IO_State: Waiting for source to send event
                    Master_Host: 127.0.0.1
                    Master_User: synctest
                    Master_Port: 3306
                    Connect_Retry: 60
                Master_Log_File: ON.000004
            Read_Master_Log_Pos: 346
                Relay_Log_File: Bean-relay-bin.000002
                    Relay_Log_Pos: 319
            Relay_Master_Log_File: ON.000004
                Slave_IO_Running: Yes
                Slave_SQL_Running: Yes
                Replicate_Do_DB:
            Replicate_Ignore_DB:
            Replicate_Do_Table:
        Replicate_Ignore_Table:
        Replicate_Wild_Do_Table:
    Replicate_Wild_Ignore_Table:
                    Last_Errno: 0
                    Last_Error:
                    Skip_Counter: 0
            Exec_Master_Log_Pos: 346
                Relay_Log_Space: 528
                Until_Condition: None
                Until_Log_File:
                    Until_Log_Pos: 0
            Master_SSL_Allowed: No
            Master_SSL_CA_File:
            Master_SSL_CA_Path:
                Master_SSL_Cert:
                Master_SSL_Cipher:
                Master_SSL_Key:
            Seconds_Behind_Master: 0
    Master_SSL_Verify_Server_Cert: No
                    Last_IO_Errno: 0
                    Last_IO_Error:
                Last_SQL_Errno: 0
                Last_SQL_Error:
    Replicate_Ignore_Server_Ids:
                Master_Server_Id: 1
                    Master_UUID: 50582deb-3efc-4ee6-8a7d-4f69f1651a91
                Master_Info_File: mysql.slave_master_info
                        SQL_Delay: 0
            SQL_Remaining_Delay: NULL
        Slave_SQL_Running_State: Replica has read all relay log; waiting for more updates
            Master_Retry_Count: 86400
                    Master_Bind:
        Last_IO_Error_Timestamp:
        Last_SQL_Error_Timestamp:
                Master_SSL_Crl:
            Master_SSL_Crlpath:
            Retrieved_Gtid_Set:
                Executed_Gtid_Set:
                    Auto_Position: 0
            Replicate_Rewrite_DB:
                    Channel_Name:
            Master_TLS_Version:
        Master_public_key_path:
            Get_master_public_key: 0
                Network_Namespace:
    1 row in set, 1 warning (0.01 sec)
    ```

### 三、测试主从

1. 在主机上创建一个数据库

    ```sql
    create database testdb charset=utf8;
    ```

2. 检查从机上是否出现此表


3. 在主机上创建一张表

    ```sql
    CREATE TABLE `users` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
    `age` int DEFAULT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
    ```

4. 检查从机上是否出现此表


### 四、代码测试数据库读写分离(python+sqlalchmey)

1. 前提工作

    - 主从数据库服务开启

2. 编写py脚本


- 方案一（基于装饰器）

    ```python
    import functools
    import random
    import time

    from sqlalchemy import Column, Integer, String, create_engine
    from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

    Base = declarative_base()


    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True)
        username = Column(String(100), unique=True, nullable=False, comment="用户名")
        phone = Column(String(11), comment="手机号")


    master_engine = create_engine("mysql+pymysql://root:root@localhost:3306/shop")
    slave_engine = create_engine("mysql+pymysql://root:root@localhost:3307/shop")
    Base.metadata.create_all(master_engine)
    Session = scoped_session(sessionmaker(bind=master_engine))


    def read_slave(f):
        @functools.wraps(f)
        def wrpper(*args, **kwargs):
            old = Session.bind
            try:
                Session.bind = slave_engine
                return f(*args, **kwargs)
            except Exception as e:
                print(e.args)
            finally:
                Session.bind = old
        return wrpper


    @read_slave
    def read_data():
        print(f"use engine {Session.bind.url}")
        objs = Session.query(User).all()
        print([{obj.id: obj.username for obj in objs}])


    def write_data():
        print(f"use engine {Session.bind.url}")
        user = User(username=f"tom-{time.time()}", phone=random.randint(0, 100))
        Session.add(user)
        Session.commit()
        print(f"add user: {user.id}")


    def main():
        write_data()
        read_data()


    if __name__ == "__main__":
        main()
    ```

- 方案二（基于自定义Session类）

    ```python
    import random
    import time

    from sqlalchemy import Column, Integer, String, create_engine
    from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
    from sqlalchemy.orm.session import Session as Se
    from sqlalchemy.sql import Delete, Insert, Update

    Base = declarative_base()


    class User(Base):
        __tablename__ = 'users'

        id = Column(Integer, primary_key=True)
        username = Column(String(100), unique=True, nullable=False, comment="用户名")
        phone = Column(String(11), comment="手机号")


    master_engine = create_engine("mysql+pymysql://root:root@localhost:3306/shop")
    slave_engine = create_engine("mysql+pymysql://root:root@localhost:3307/shop")
    Base.metadata.create_all(master_engine)


    class CustomSe(Se):

        def get_bind(self, mapper=None, clause=None, bind=None, _sa_skip_events=None, _sa_skip_for_implicit_returning=False, **kw):
            if self._flushing or isinstance(clause, (Update, Delete, Insert)):
                print("insert update delete engine: ", master_engine.url)
                return master_engine

            print("query engine: ", slave_engine.url)
            return slave_engine


    Session = scoped_session(sessionmaker(class_=CustomSe))


    def read_data():
        objs = Session.query(User).all()
        print([{obj.id: obj.username for obj in objs}])


    def write_data():
        user = User(username=f"tom-{time.time()}", phone=random.randint(0, 100))
        Session.add(user)
        Session.commit()
        print(f"add user: {user.id}")


    def main():
        write_data()
        read_data()


    if __name__ == "__main__":
        main()
    ```