## 一、事务

- 相关命令集合

  - 开启事务 multi

  - 执行事务 exec

  - 取消事务 discard

  - watch 标记所有指定的key，配合事务充当乐观锁使用

- Redis 事务注意点：

  - 批量操作在发送 EXEC 命令前被放入队列缓存。

  - 收到 EXEC 命令后进入事务执行，事务中任意命令执行失败，其余的命令依然被执行。

  - 在事务执行过程，其他客户端提交的命令请求不会插入到事务执行命令序列中。

- **小细节点**：单个 Redis 命令的执行是原子性的，但 Redis 没有在事务上增加任何维持原子性的机制，所以 Redis 事务的执行并不是原子性的。

  - redis在执行事务时，语法的错误不会导致其他值进行改变（编译性错误）

    原因很好解释，因为根本没办法执行

    ```bash
    127.0.0.1:6379> set name tom
    OK
    127.0.0.1:6379> MULTI
    OK
    127.0.0.1:6379(TX)> set age 12
    QUEUED
    127.0.0.1:6379(TX)> sets sex boy	# 语法错误
    (error) ERR unknown command `sets`, with args beginning with: `sex`, `boy`,
    127.0.0.1:6379(TX)> exec	# 执行事务，由于语法的异常，导致事务无法正常执行
    (error) EXECABORT Transaction discarded because of previous errors.
    127.0.0.1:6379> get age	# 根据此处可知，事务执行失败
    (nil)
    ```

    

  - 类型的错误会导致其他值进行改变（运行时错误）

    ```bash
    127.0.0.1:6379> set name tom
    OK
    127.0.0.1:6379> MULTI
    OK
    127.0.0.1:6379(TX)> set age 12
    QUEUED
    127.0.0.1:6379(TX)> incr name	# 类型故意设定错误，并进行自增加操作
    QUEUED
    127.0.0.1:6379(TX)> exec
    1) OK
    2) (error) ERR value is not an integer or out of range
    127.0.0.1:6379> get age	# 明显事务中的age被执行成功了
    "12"
    ```

  - 通过watch实现乐观锁

    这里需要在客户端1执行`watch age`之后，`exec`之前，执行完毕客户端2的所有内容

    ```bash
    # 客户端1
    127.0.0.1:6379> get age
    "110"
    127.0.0.1:6379> WATCH age	# 开启对age的监控
    OK
    127.0.0.1:6379> MULTI
    OK
    127.0.0.1:6379(TX)> INCR age
    QUEUED
    127.0.0.1:6379(TX)> set name jerry
    QUEUED
    127.0.0.1:6379(TX)> EXEC	# 由于age被监控，在客户端2中被修改了，redis将会放弃这部分的事务操作，导致事务执行失败
    (nil)
    127.0.0.1:6379> get name	# 证明事务执行失败,所有操作将不会被执行
    (nil)
    127.0.0.1:6379> UNWATCH	# 取消监视，事实上 不管事务是否成功执行， 对所有键的监视都会被取消
    OK
    ```

    ```bash
    # 客户端2
    127.0.0.1:6379> get age
    "110"
    127.0.0.1:6379> INCR age
    (integer) 111
    ```

## 二、补充

...



