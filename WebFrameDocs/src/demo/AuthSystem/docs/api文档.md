### 一、用户注册

`/register/` POST

所需参数

| username | 用户名 |      |
| -------- | ------ | ---- |
| email    | 邮箱   |      |
| password | 密码   |      |

返回数据格式

```json
{
    "code": 200,
    "message": "注册成功",
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Ilx1NWMwZlx1NjYwZSIsImVtYWlsIjoiMTczNzE0MzgyMjdAMTIyLmNvbSIsImV4cCI6MTYzMzQyOTc2MH0.wOlkq43bbxqCwE7j8AgWUoAGdJN66Mg-sGMethZxw1s",
        "username": "小明",
        "email": "17371438227@122.com"
    }
}
```



### 二、用户登录

`/login/?secret_id=xxx&redirect_uri=xxx` POST

所需参数

| username | 用户名 | usernam和email二选一 |
| -------- | ------ | -------------------- |
| email    | 邮箱   |                      |
| password | 密码   |                      |

返回数据格式

```json
{
    "code": 200,
    "message": "登录成功",
    "data": {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Ilx1NWMwZlx1NjYwZSIsImVtYWlsIjoiMTczNzE0MzgyMjdAMTIyLmNvbSIsImV4cCI6MTYzNTI2OTc2N30.lkz7WUQ4QbOVQRuTeHoaNSnyIK7x-lbWfruZYsxn96w",
        "redirect_uri": "",
        "authorization_code": "",
        "username": "小明",
        "email": "17371438227@122.com"
    }
}
```



### 三、用户权限

1. 获取个人信息 `/auth/` GET

所需参数

| Authorization | 用户token |      |
| ------------- | --------- | ---- |

返回数据格式

```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "username": "小明",
        "email": "17371438227@122.com",
        "secret_id": "MTYzNTI1NzAwNC41MDM4NDI=",
        "secret_value": "7f02f2cd2aa0ccbb3417b9afb67c572199643452e2aa1a1ffbba60d1b32744ab"
    }
}
```

2. 更改为开发者`/auth/` PATCH

所需参数

| Authorization    | 用户token |      |
| ---------------- | --------- | ---- |
| **is_developer** | **true**  |      |

返回数据格式

```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "username": "小明",
        "email": "17371438227@122.com",
        "secret_id": "MTYzNTI1NzAwNC41MDM4NDI=",
        "secret_value": "7f02f2cd2aa0ccbb3417b9afb67c572199643452e2aa1a1ffbba60d1b32744ab"
    }
}
```

### 四、授权调用

1. 用户授权页面 `/oauth/` GET

所需参数

| secret_id    | MTYzNTI1NzAwNC41MDM4NDI= |      |
| ------------ | ------------------------ | ---- |
| redirect_uri | http://example.com       |      |

返回数据格式

```json
重定向到授权登录页
```

2. 客户端后端调用 `/oauth/` POST

所需参数

| secret_id    | MTYzNTI1NzAwNC41MDM4NDI=                                     |      |
| ------------ | ------------------------------------------------------------ | ---- |
| secret_value | 7f02f2cd2aa0ccbb3417b9afb67c572199643452e2aa1a1ffbba60d1b32744ab |      |
| authorization_code         | 6b7187a1-f5d7-4ebe-a222-c36a939fad36                         |      |

返回数据格式

```json
{
    "code": 200,
    "message": "获取授权成功",
    "data": {
        "username": "小明",
        "email": "17371438227@122.com"
    }
}
```

