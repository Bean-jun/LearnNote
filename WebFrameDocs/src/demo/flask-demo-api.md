# api文档



源码地址：`WebFrameDocs/src/demo`  下  `flask-demo`



以下api前缀均为： `/api/v1`


### 一、账户

1. 注册 `/register` POST

   | username    | 用户名   |
   | ----------- | -------- |
   | email       | 邮箱     |
   | pwd         | 密码     |
   | confirm_pwd | 重复密码 |
   
   响应数据格式
   
   ```JSON
   {
       "code": 200,
       "message": "注册成功",
       "data": {
           "username": "17371432327@qq.com",
           "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjE3MzcxNDMyMzI3QHFxLmNvbSIsImVtYWlsIjoiMTczNzE0MzIzMjdAcXEuY29tIiwiZXhwIjoxNjMyOTMwNDQwfQ.UMYG-FddzDqPmL8fG7Gm_os1Ug1ppACQORjP7ij9D20"
       }
   }
   ```
   
   
   
2. 登录 `/login `   POST

    | username | 用户名 | 当前字段可以传入用户名或者邮箱 |
    | -------- | ------ | ------------------------------ |
    | pwd      | 密码   |                                |

    响应数据格式

    ```json
    {
        "code": 200,
        "message": "登录成功",
        "data": {
            "username": "17371432327@qq.com",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjE3MzcxNDM4MjI3QDE2My5jb20iLCJlbWFpbCI6IjE3MzcxNDM4MjI3QDE2My5jb20iLCJleHAiOjE2MzI5MzA0NTN9.KNsxXXLFtICn6K6YTbv6NCMwDKONLjl7IkAGBVRiQpk"
        }
    }
    ```

    

3. 修改密码 `/mPassword `  POST

    | username    | 用户名     | 当前字段可以传入用户名或者邮箱 |
    | ----------- | ---------- | ------------------------------ |
    | old_pwd     | 旧密码     |                                |
    | pwd         | 新密码     |                                |
    | confirm_pwd | 重复新密码 |                                |

    响应数据格式

    ```json
    {
        "code": 200,
        "message": "修改成功",
        "data": {
            "username": "17371432327@qq.com",
            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjE3MzcxNDMyMzI3QHFxLmNvbSIsImVtYWlsIjoiMTczNzE0MzIzMjdAcXEuY29tIiwiZXhwIjoxNjMyOTMwNTA5fQ.KGdRerrbC5ebqk6i-HbhzUWtX5VO6IvKqqWGWqGfISY"
        }
    }
    ```

    

### 二、博客

1. 获取博客分类列表 `/blogCategory` GET

   响应数据格式

   ```json
   {
       "code": 200,
       "message": "获取成功",
       "data": [
           {
               "id": 2,
               "name": "python"
           },
           {
               "id": 3,
               "name": "java"
           },
           {
               "id": 9,
               "name": "abc"
           },
           {
               "id": 10,
               "name": "abcasd"
           }
       ]
   }
   ```

   

2. 添加博客分类 `/blogCategory`	POST

   | token    | 请放在请求头中 |
   | -------- | -------------- |
   | category | 分类名称       |

   响应数据格式

   ```json
   {
       "code": 200,
       "message": "添加成功",
       "data": {
           "categoryId": 15,
           "category": "python入门到入土"
       }
   }
   ```

   

3. 删除博客分类 `/blogCategory`  DELETE

   | token    | 请放在请求头中 |
   | -------- | -------------- |
   | category | 分类名称       |

   响应数据格式

   ```json
   {
       "code": 200,
       "message": "数据不存在",
       "data": ""
   }
   
   {
       "code": 200,
       "message": "删除成功",
       "data": ""
   }
   ```

   

4. 获取博客列表 `/blog` GET

   ```json
   {
       "code": 200,
       "message": "获取成功",
       "data": [
           {
               "id": 5,
               "title": "python入门到入土"
           },
           {
               "id": 40,
               "title": "golang"
           }
       ]
   }
   ```

   

5. 添加博客`/blog` POST

   | token     | 请放在请求头中 |      |
   | --------- | -------------- | ---- |
   | category  | 博客分类       |      |
   | title     | 博客标题       |      |
   | content   | 博客内容       |      |
   | top_image | 博客首页头像   |      |

   响应数据格式

   ```json
   {
       "code": 200,
       "message": "添加成功",
       "data": {
           "categoryId": 51,
           "category": "python入门到入土",
           "titleId": 51,
           "title": "小白编程5",
           "content": "adsfasdfasdg",
           "top_image": "https://images.cnblogs.com/cnblogs_com/xujunkai/1927362/o_210203025041微信图片_20210203104952.jpg"
       }
   }
   ```

   

6. 获取单条博客 `/blog/<int:id>` GET

   响应数据格式

   ```json
   {
       "code": 200,
       "message": "获取成功",
       "data": {
           "categoryId": 47,
           "category": "python入门到入土",
           "titleId": 47,
           "title": "小白编程",
           "content": "adsfasdfasdg",
           "top_image": "https://images.cnblogs.com/cnblogs_com/xujunkai/1927362/o_210203025041微信图片_20210203104952.jpg"
       }
   }
   ```

   

7. 修改单条博客`/blog/<int:id>` PUT

   | token     | 请放在请求头中 |      |
   | --------- | -------------- | ---- |
   | category  | 博客分类       |      |
   | title     | 博客标题       |      |
   | content   | 博客内容       |      |
   | top_image | 博客首页头像   |      |

   响应数据格式

   ```json
   {
       "code": 200,
       "message": "修改成功",
       "data": {
           "categoryId": 47,
           "category": "python入门到入土",
           "titleId": 47,
           "title": "小白编程abcd",
           "content": "adsfasdfasdg",
           "top_image": "https://images.cnblogs.com/cnblogs_com/xujunkai/1927362/o_210203025041微信图片_20210203104952.jpg"
       }
   }
   ```

   

8. 删除单条博客`/blog/<int:id>` DELETE

   | token | 请放在请求头中 |      |
   | ----- | -------------- | ---- |

   响应数据格式

   ```json
   {
       "code": 200,
       "message": "删除成功",
       "data": ""
   }
   ```

   

