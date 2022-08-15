### 一、SQL语句分类

- DCL(Data Control Language)：数据控制语言，用来定义访问权限和安全级别。

  >1. 创建用户
  >
  >  <pre>create user 用户名@地址 identified by 密码;</pre>
  >  <pre>create user 用户名@地址 identified with mysql_native_password by 密码;</pre>
  >
  >2. 删除用户
  >
  >   <pre>drop user 用户名@地址</pre>
  >
  >3. 给用户授权
  >
  >  <pre>grant 权限1，…，权限n on 数据库.* to 用户名@地址;</pre>
  >
  >  例如：
  >
  >  <pre>grant select on blog_db.* to user@localhost;</pre>
  >
  >4. 撤销授权
  >
  >  <pre>revoke 权限1，…，权限n on 数据库.* from 用户名@地址;</pre>
  >
  >5. 查看用户权限
  >
  >  <pre>show grants for 用户名@IP地址</pre>
  >
  >6. 修改用户密码
  >
  >  <pre>set password for 用户名@地址 = password(新密码); // mysql 5.7</pre>
  >
  >  <pre>set password for 用户名@地址 = 新密码; // mysql 8.0</pre>
  >
  >7. 刷新权限
  >  <pre>flush privileges;</pre>
  >

- DDL(Data Definition Language)：数据定义语言，用来定义数据库对象：库、表、列等。功能：创建、删除、修改库和表结构。

  >1. 创建表
  >
  >   ```mysql
  >   -- 班级表
  >   create table `cs_class` (
  >   	`autoid` int auto_increment,
  >     `name` varchar(100),
  >     `state` bool default true,
  >     primary key(autoid)
  >   );
  >   -- 学生表
  >   create table `cs_student` (
  >   	`autoid` int auto_increment,
  >     `c_autoid` int,
  >     `name` varchar(100),
  >     `gender` char,
  >     `state` bool default true,
  >     primary key(autoid),
  >     foreign key (c_autoid) references cs_class(autoid)
  >   );
  >   ```
  >
  >2. 对表结构操作
  >
  >   ```mysql
  >   -- 添加列
  >   alter table cs_class add address varchar(200);
  >   -- 删除列
  >   alter table cd_class drop address;
  >   -- 修改字段
  >   alter table cs_class modify name varchar(200);
  >   -- 修改字段&字段名
  >   alter table cs_class change name cs_name varchar(100);
  >   -- 添加外键约束
  >   alter table cs_student constraint foreign key (f_autoid) references cs_class(autoid);	-- 需要提前在该表中添加一个f_autoid字段
  >   -- 修改表名
  >   alter table cs_class rename new_cs_class;
  >   -- 删除表
  >   alter drop if exists cs_class;
  >   ```

- DML(Data Manipulation Language)：数据操作语言，用来定义数据库记录：增、删、改表记录。

  >1. 添加数据
  >
  >   ```mysql
  >   insert into cs_class (name) values ('六年级一班'), ('六年级二班');
  >   ```
  >
  >2. 删除数据
  >
  >   ```mysql
  >   delete from cs_class where autoid=1;
  >   ```
  >
  >3. 修改数据
  >
  >   ```mysql
  >   update cs_class set name="六年级一班" where autoid=2;
  >   ```
  >
  >4. delete、drop、truncate对比
  >
  >   ```mysql
  >   当表被truncate后，表和索引的所占空间会恢复到初始大小，delete操作不会减少表和索引的所占空间。
  >   truncate和delete只删除数据，drop则删除整个表（结构和数据）。
  >   truncate速度快，效率高，可以理解为先把表删除了，再重新建立。
  >   truncate和delete均不会使表结构及其列、约束、索引等发生改变。
  >   ```
  >
  >   

- DQL(Data Query Language)：数据查询语言，用来查询记录。



### 二、触发器

触发器（Trigger）是与表有关的数据库对象，是一种特殊的存储过程，在满足定义条件时触发，并执行触发器中定义的语句集合。它可以在你执行INSERT、UPDATE或DELETE的时候，执行一些特定的操作。在创建触发器时，可以指定是在执行SQL语句之前或是之后执行这些操作。

1. 基础语法

    ```shell
    # 创建触发器
    CREATE TRIGGER <触发器名称>
    { BEFORE | AFTER }
    { INSERT | UPDATE | DELETE } 
    ON <表名称>
    FOR EACH ROW
    BEGIN
    <触发的SQL语句>
    END;
    # 查看触发器
    SHOW TRIGGERS [FROM schema_name];
    # 删除触发器
    DROP TRIGGER [IF EXISTS] [schema_name.]trigger_name;
    ```

2. Demo

    有一张users表，在对其表进行插入、修改、删除时，自动将将操作日志写入到logs表中

    ```sql
    -- 创建一张用户表
    CREATE TABLE `users` ( 
      `id` BIGINT PRIMARY KEY AUTO_INCREMENT, 
      `name` VARCHAR(30) NOT NULL, 
      `createAt` datetime, 
      `modifyAt` datetime, 
      `state` bool DEFAULT TRUE 
    );

    -- 创建一张操作日志表
    CREATE TABLE `logs` (
      `id` BIGINT PRIMARY KEY AUTO_INCREMENT, 
      `targetable` VARCHAR(30) NOT NULL,
      `method` VARCHAR(30) NOT NULL,
      `createAt` datetime, 
      `modifyAt` datetime, 
      `state` bool DEFAULT TRUE 
    );

    -- 创建用户表的触发器，当用户表crud时，在日志表中生成记录
    CREATE TRIGGER `users_trigger_insert` AFTER INSERT ON `users` FOR EACH ROW
    BEGIN
        INSERT INTO `logs` ( `targetable`, `method`, `createAt`, `modifyAt` )
      VALUES("users", "insert", NOW(), NOW());
    END;

    CREATE TRIGGER `users_trigger_update` AFTER UPDATE ON `users` FOR EACH ROW
    BEGIN
        INSERT INTO `logs` ( `targetable`, `method`, `createAt`, `modifyAt` )
      VALUES("users", "update", NOW(), NOW());
    END;

    CREATE TRIGGER `users_trigger_delete` AFTER DELETE ON `users` FOR EACH ROW
    BEGIN
        INSERT INTO `logs` ( `targetable`, `method`, `createAt`, `modifyAt` )
      VALUES("users", "delete", NOW(), NOW());
    END;

    -- 查看触发器
    SHOW TRIGGERS;

    -- 插入数据
    INSERT INTO `users` (`name`, `createAt`, `modifyAt`) values ("张三", NOW(), NOW());
    INSERT INTO `users` (`name`, `createAt`, `modifyAt`) values ("李四", NOW(), NOW());
    INSERT INTO `users` (`name`, `createAt`, `modifyAt`) values ("李四22", NOW(), NOW());
    UPDATE `users` set `name`="张三1" WHERE `name`="张三";
    UPDATE `users` set `name`="李四1" WHERE `name`="李四";
    DELETE FROM `users` WHERE `name`="李四22";

    -- 删除触发器
    DROP TRIGGER `users_trigger_insert`;
    DROP TRIGGER `users_trigger_update`;
    DROP TRIGGER `users_trigger_delete`;

    -- 请自行查看表中数据
    ```

### 三、索引

1. 索引种类

- 普通索引 -->加速查找
- 主键索引 -->加速查找 + 不能为空 + 不能重复
- 唯一索引 -->加速查找 + 不能重复
- 联合索引

    > 联合唯一索引
    >
    > 联合主键索引
    >
    > 联合普通索引

2. 索引创建 (help CREATE INDEX)

    ```mysql
    -- 创建普通索引
    create index 索引名 on 表名(列名);
    -- 创建唯一索引
    create unique index 索引名 on 表名(列名);
    -- 创建联合索引
    create index 索引名 on 表名(列名,列名);
    -- 删除索引
    drop index 索引名 on 表名;
    -- 查看索引
    show index from 表名;
    ```

3. 索引失效情况

- 如果条件中有or，即使其中有条件带索引也不会使用走索引，除非全部条件都有索引
- 复合索引不满足最左原则就不能使用全部索引
- like查询以%开头
- 存在列计算
- 如果mysql估计使用全表扫描要比使用索引快，则不使用索引，比如结果的量很大
- 存在类型转化


### 四、事务

1. 四大特性(ACID)

    ```shell
    1.1 原子性(一个事务（transaction）中的所有操作，要么全部完成，要么全部不完成，不会结束在中间某个环节。)
    
    1.2 一致性(在事务【开始之前和结束以后】，数据库的完整性没有被破坏，数据库状态应该与业务规则保持一致。)
    
    1.3 隔离性(数据库【允许多个并发事务同时对其数据进行读取和修改】，隔离性可以防止多个事务在并发修改共享数据时产生【数据不一致】的现象。)
    
    事务隔离级别分为不同等级，包括读未提交（Read uncommitted）、读提交（read committed）、可重复读（repeatable read）和串行化（Serializable）
    
    1.4 持久性(事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。)
    ```
    
2. 事务的隔离级别

    |                              |      |            |      |                                            |
    | ---------------------------- | ---- | ---------- | ---- | ------------------------------------------ |
    | 隔离级别                     | 脏读 | 不可重复读 | 幻读 | 解决方案                                   |
    | Read uncommitted（读未提交） | √    | √          | √    |                                            |
    | Read committed（读已提交）   | ×    | √          | √    | undo log                                   |
    | Repeatable read（可重复读）  | ×    | ×          | √    | MVCC版本控制+间隙锁（mysql的rr不存在幻读） |
    | Serializable（串行化）       | ×    | ×          | ×    |                                            |

    脏读：一个事务读到了其他事务未提交的数据，未提交意味着这些数据可能会回滚，读到的数据不一定准确。

    不可重复读：【一个事务】（A事务）修改了【另一个未提交事务】（B事务）读取过的数据。那么B事务【再次读取】，会发现两次读取的数据不一致。也就是说在一个原子性的操作中一个事务两次读取相同的数据，却不一致，一行数据不能重复被读取。主要是【update】语句，会导致不可重复读。

    幻读: 一个事务按照某些条件进行查询，事务提交前，有另一个事务插入了满足条件的其他数据，再次使用相同条件查询，却发现多了一些数据，就像出现了幻觉一样。幻读主要针对针对delete和insert语句。

    不可重复读强调的是两次读取的数据【内容不同】，幻读强调的是两次读取的【行数不同】。

    ```mysql
    -- 查看全局和当前事务的隔离级别
    SELECT @global.transaction_isolation, @transaction_isolation_isolation;
    show variables like 'transaction_isolation';
    --5.7   tx_isolation
    --8.0   transaction_isolation

    -- 设置下一个事务的隔离级别
    SET transaction isolation level read uncommitted;
    SET transaction isolation level read committed;
    set transaction isolation level repeatable read;
    SET transaction isolation level serializable;
    -- 设置当前会话的隔离级别
    SET session transaction isolation level read uncommitted;
    SET session transaction isolation level read committed;
    set session transaction isolation level repeatable read;
    SET session transaction isolation level serializable;
    -- 设置全局事务的隔离级别
    SET GLOBAL transaction isolation level read uncommitted;
    SET GLOBAL transaction isolation level read committed;
    set GLOBAL transaction isolation level repeatable read;
    SET GLOBAL transaction isolation level serializable;
    ```


3. 事务的一些操作

- 3.1 显式事务和隐式事务

  ```mysql
  -- mysql默认开启隐式事务，可通过 autocommit变量查看
  SHOW VARIABLES LIKE "autocommit";
  -- 开启事务
  begin; 或者 start transaction;
  -- 提交事务
  commit;
  --回滚事务
  rollback;
  ```

- 3.2 只读事务

    ```mysql
    start transaction read only;
    commit;
    ```

- 3.3 保存点

    ```mysql
    start transaction;
    savepoint a;
    rollback to a;
    commit;
    ```