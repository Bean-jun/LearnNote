### 1. 链接数据库

```python
# SQLAlchemy本身无法操作数据库，其必须以来pymsql等第三方插件，Dialect用于和数据API进行交流，根据配置文件的不同调用不同的数据库API，从而实现对数据库的操作，如：

# https://docs.sqlalchemy.org/en/14/dialects/index.html

# MySQL-Python 
#     mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
# 
# pymysql 
#     mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
# 
# MySQL-Connector 
#     mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
# 
# cx_Oracle 
#     oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]
```

### 2. 使用原生sql

*   使用 Engine/ConnectionPooling/Dialect 进行数据库操作，Engine使用ConnectionPooling连接数据库，然后再通过Dialect执行SQL语句。

```python
# -*- coding:utf-8 -*-
from sqlalchemy import create_engine

# 链接数据库
engine = create_engine("mysql+pymysql://root:123@127.0.0.1:3306/t1", max_overflow=5)

# 执行SQL
# cur = engine.execute(
#     "INSERT INTO hosts (host, color_id) VALUES ('1.1.1.22', 3)"
# )

# 新插入行自增ID
# cur.lastrowid

# 执行SQL
# cur = engine.execute(
#     "INSERT INTO hosts (host, color_id) VALUES(%s, %s)",[('1.1.1.22', 3),('1.1.1.221', 3),]
# )


# 执行SQL
# cur = engine.execute(
#     "INSERT INTO hosts (host, color_id) VALUES (%(host)s, %(color_id)s)",
#     host='1.1.1.99', color_id=3
# )

# 执行SQL
# cur = engine.execute('select * from hosts')
# 获取第一行数据
# cur.fetchone()
# 获取第n行数据
# cur.fetchmany(3)
# 获取所有数据
# cur.fetchall()
```

### 2. 使用orm实现对数据库的操作

*   使用 ORM/Schema Type/SQL Expression Language/Engine/ConnectionPooling/Dialect 所有组件对数据进行操作。根据类创建对象，对象转换成SQL，执行SQL。

#### 2.1 创建表结构

```python
"""
注意对于一对多及多对多的结构，使用relationship来实现关联，方便后期的数据查询及添加

# 例如
cls = relationship("Classes", backref='student')    # 一对多的实现
servers = relationship('Server', secondary='server2group', backref='groups')  # 多对多需要添加secondary字段

"""
import datetime

from sqlalchemy import String, Column, Integer, DateTime, ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base

# 链接数据库
engine = create_engine("mysql+pymysql://root:00090009@192.168.199.103:3306/sqlalchemy?charset=utf8", max_overflow=5)
Base = declarative_base()


class Classes(Base):
    """创建班级表"""
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, unique=True)


# 一对多实例
class Student(Base):
    """创建学生表"""
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    ctime = Column(DateTime, default=datetime.datetime.now)
    class_id = Column(Integer, ForeignKey('classes.id'))


# 多对多实例
class Hobby(Base):
    """爱好"""
    __tablename__ = 'hobby'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caption = Column(String(32), default="看鸡你太美")


"""
sqlalchemy对于多对多需要手动创建第三张表
"""


class Student2Hobby(Base):
    """学生爱好表"""
    __tablename__ = 'student2hobby'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    hobby_id = Column(Integer, ForeignKey('hobby.id'))

    __table_args__ = (
        UniqueConstraint('student_id', 'hobby_id', name='uix_student_id_hobby_id'),  # 创建联合索引
    )


def init_db():
    # 创建表
    Base.metadata.create_all(engine)


def drop_db():
    # 删除表
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    init_db()
    drop_db()
```

#### 2.2 操作表

注意：以下操作都必须在`创建链接`和`关闭链接`之间完成

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 链接数据库
engine = create_engine("mysql+pymysql://root:00090009@192.168.199.103:3306/sqlalchemy?charset=utf8", max_overflow=5)

# 创建链接
Session = sessionmaker(bind=engine)
session = Session()

"""
增加、修改、删除、查询
"""

# 关闭链接
session.close()
```

*   增加

```python
session.add(Classes(name='三年级二班'))  # 单条
session.add_all([  # 多条增加
    Classes(name='三年级1班'),
    Classes(name='三年级2班'),
    Classes(name='三年级3班')
])
session.commit()
```

*   查询

```python
res = session.query(Classes).all()
print(res)
res = session.query(Classes).filter(Classes.id == 1).all()
print(res)
res = session.query(Classes).filter_by(Classes.id = 1).all()
print(res)
```

*   修改
    *   特殊设置
        *   synchronize\_session=False # 加在其中表示字符串拼接
        *   synchronize\_session="evaluate"  # 加在其中表示数字相加

```python
session.query(Classes).filter(Classes.id == 1).update({Classes.name: '三年级0班'})
session.query(Classes).filter(Classes.id == 2).update({Classes.name: '三年级0班'}，synchronize_session = False)
session.commit()
```

*   删除

```python
session.query(Classes).filter(Classes.id == 4).delete()
session.commit()
```

#### 2.3 查询中的其他操作

```python
from sqlalchemy import and_, or_

ret = session.query(Users).filter(and_(Users.id > 3, Users.name == 'eric')).all()
ret = session.query(Users).filter(or_(Users.id < 2, Users.name == 'eric')).all()
ret = session.query(Users).filter(
    or_(
        Users.id < 2,
        and_(Users.name == 'eric', Users.id > 3),
        Users.extra != ""
    )).all()

# 通配符
ret = session.query(Users).filter(Users.name.like('e%')).all()
ret = session.query(Users).filter(~Users.name.like('e%')).all()

# 正则
db.session.query(Users).filter(User.name.op('regexp')(r'[[:<:]]John[[:>:]]')).all() 

# 限制
ret = session.query(Users)[1:2]

# 排序
ret = session.query(Users).order_by(Users.name.desc()).all()
ret = session.query(Users).order_by(Users.name.desc(), Users.id.asc()).all()

# 分组
from sqlalchemy.sql import func

ret = session.query(Users).group_by(Users.extra).all()
ret = session.query(
    func.max(Users.id),
    func.sum(Users.id),
    func.min(Users.id)).group_by(Users.name).all()

ret = session.query(
    func.max(Users.id),
    func.sum(Users.id),
    func.min(Users.id)).group_by(Users.name).having(func.min(Users.id) > 2).all()

# 连表

ret = session.query(Users, Favor).filter(Users.id == Favor.nid).all()

ret = session.query(Person).join(Favor).all()

ret = session.query(Person).join(Favor, isouter=True).all()

# 组合
q1 = session.query(Users.name).filter(Users.id > 2)
q2 = session.query(Favor.caption).filter(Favor.nid < 2)
ret = q1.union(q2).all()

q1 = session.query(Users.name).filter(Users.id > 2)
q2 = session.query(Favor.caption).filter(Favor.nid < 2)
ret = q1.union_all(q2).all()
```

#### 2.4 关联关系介绍

[https://www.cnblogs.com/DragonFire/p/10166527.html](https://www.cnblogs.com/DragonFire/p/10166527.html)

