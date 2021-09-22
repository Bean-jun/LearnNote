## 一、字符串
- 添加键值
	
	- set key value
	
- 查询键值
	- get key
	- 查询所有的键
		- keys *
	
- 往值中添加内容
	
	- append key need_append_data
	
- NX操作
	- 一般用法
		- set key value NX 处理之后，内容若是存在则不修改；不存在则添加
	
- 针对数字可以尝试修改

  - incr key  可以将字符串的数字增加1
  - decr key 可以将字符串的数字减少1
  - incrby key n  可以将字符串的数字增加n
  - decr key n   可以将字符串的数字减少n

- 删除
  - del key 

- Python中的操作

  ```python
  import redis
  
  # 连接数据库
  client = redis.Redis(host='', port=6379, decode_responses=True)
  # 设置键值对
  client.set('name', '小明')
  client.set('age', 12)
  client.incr('age', 1) # 对age这个字段进行增加1  
  for key in client.keys():
  		print(key)
  ```



## 二、列表    

- 添加键值

	- lpush key value1 value2 value3 ... # 左侧插入
	- rpush key value1 value2 value3 ... # 右侧插入

- 查询键值

	- llen key # 直接查看键对应值的长度
	- lrange key start stop # 支持索引查询 注意：包含stop

- 弹出数据

	- lpop # 左侧弹出
	- rpop # 右侧弹出

- 修改键值

	- lset key index value # 将index位置的values进行更新
	
- Python中的操作

  ```python
  import redis
  
  
  if __name__ == '__main__':
      client = redis.Redis(host='', port=6379, decode_responses=True)
      # 左侧插入
      client.lpush('student', '小米', '狗剩', '郝大力')
      # 获取长度
      reslen = client.llen('student')
      # 获取结果
      res = client.lrange('student', 0, -1)
      print('当前长度为%s  结果为%s' % (reslen, res))
      # 左侧弹出
      client.lpop('student')
      # 右侧弹出
      client.rpop('student')
      reslen = client.llen('student')
      res = client.lrange('student', 0, -1)
      print('当前长度为%s  结果为%s' % (reslen, res))
      # 修改内容
      client.lset('student', 0, '狗大力')
      res = client.lrange('student', 0, -1)
      print('当前长度为%s  结果为%s' % (reslen, res))
  ```



## 三、集合

- 添加键值
  - sadd key value1 value2 value3 ... # 往集合中插入数据
- 查询键值
  - scard key 	# 查询集合长度
  - spop key count      # count表示想要取到的数据个数，默认一条
    - 注意：这个操作`会`清空集合中的数据，在Python中以list表现
  - smembers key      # 获取所有的集合
    - 注意：这个操作`不会`清空集合中的数据，在Python中以set表现
  - sismember key value      # 判断value是否为key中的内容
    - 注意：存在返回1，不存在返回0
    - 在Python中交互，存在返回True，不存在返回False
- 删除数据
  - srem key value  [value]   # 删除集合中的value值

- 集合的一部分操作
  - 交集
    - sinter key key [key]
  - 并集
    - sunion key key [key]
  - 差集
    - sdiff sunion key key [key]

- Python 中的操作

  ```python
  import redis
  
  
  if __name__ == '__main__':
      client = redis.Redis(host='', port=6379, decode_responses=True)
      # 添加数据
      client.sadd('tset', '西瓜', '苹果', '香蕉', '大栗子', '西红柿', '巧克力')
      client.sadd('tset1', '西瓜', '苹果', '香蕉', '大栗子', '西红柿', '巧克力')
      client.sadd('tset2', '苹果', '香蕉', '苦瓜')
      print(client.scard('tset'))
      # 弹出数据
      res = client.spop('tset', 1)
      print("弹出内容为%s" % res)
      # 查询内容
      res = client.smembers('tset')
      print("还有内容%s" % res)
      # 判断内容是否在集合中
      flag = client.sismember('tset', '香蕉')
      print("香蕉是否在%s" % flag)
      # 删除内容
      client.srem('tset', '巧克力')
      res = client.smembers('tset')
      print("还有内容%s" % res)
      # 差看交集
      res = client.sinter('tset1', 'tset2')
      print("交集结果为%s" % res)
      # 查看并集
      res = client.sunion('tset1', 'tset2')
      print("并集结果为%s" % res)
      # 查看差集
      res = client.sdiff('tset1', 'tset2')
      print("差集结果为%s" % res)
  ```



## 四、哈希表

- 添加键值
  - hset key field value # 添加键值
  - hmet key field1 value1 [field2 value2] # 添加多个键值
  
- 查询内容
  - hkeys key # 获取字段
  - hget key field # 获取字段的值
  - hmget key field1 field2 ... # 获取多个字段的值
  - hgetall # 获取所有字段和值
  
- other
  - hexists key  field # 判断字段是否存在
  - hlen key # 获取键值长度


- Python中的操作
```python
import redis
import json


if __name__ == '__main__':
    client = redis.Redis(host='139.224.46.213', port=6379, decode_responses=True)
    # 添加数据
    client.hset('thash', 'tom', 1)  # 单条
    user_info = {
        'tom': json.dumps({'age': 20, 'score': 89, 'address': "武汉市"}, ensure_ascii=False),
        'jerry': json.dumps({'age': 21, 'score': 79, 'address': "江西省"}),
        'tim': json.dumps({'age': 20, 'score': 94, 'address': "天门市"}),
        '武松': json.dumps({'age': 23, 'score': 84, 'address': "钟祥市"}, ensure_ascii=False),
    }
    client.hmset('tmhash', user_info)   # 多条
    # 查询所有的字段
    res = client.hkeys('thash')
    print("当前内容为%s" % res)
    res = client.hkeys('tmhash')
    print("当前内容为%s" % res)
    # 查询字段值
    res = client.hget('tmhash', '武松')
    print("当前内容为%s" % res)
    res = client.hmget('tmhash', 'tom', '武松')
    print("当前查询多个值的内容为%s" % res)
    res = client.hgetall('tmhash')
    print("当前内容为%s" % res)
    # 判断内容是否在集合中
    flag = client.hexists('thash', 'tom')
    print("存在情况 %s" % flag)
    # 获取长度
    length = client.hlen('tmhash')
    print("长度为%s" % length)
```



## 五、 有序集合

元素都是string类型，并具有唯一性；每个元素都会关联一个double类型的score，表示元素的权重

- 添加键值
    - zadd key score1 member1 score2 member2 ...  
- 获取键值
    - 获取指定范围的元素
        - zrange key start stop
    - 获取score在指定范围的元素
        - zrangebyscore key min max
    - 获取元素的score
        - zscore key member
    - 删除指定范围的元素
        - zrem key member1 member2 ...
    - 删除指定score范围的元素
        - zremrangegyscore key min max
