### 1.1基本框架结构
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>xxx</title>
</head>
<body>
    xxx
</body>
</html>
```
### 1.2标题标签
- 通过\<h1>,\<h2>,\<h3>,\<h4>,\<h5>,\<h6>实现标题
    ```html
    <!-- exp -->
    <h1>xxx</h1>
    ```
### 1.3段落标签
- \<p>\</p>  相邻p标签间有空格
    ```html
    <p>xxx</p>
    ```
### 1.4字符实体
- 空格 \&nbsp;  少量空格时使用，多数使用css实现空格
- 大于号 \&gt;
- 小于号 \&lt;
- 换行 \<br> 或者 \<br />   后者较为规范
### 1.5块标签
- \<div> 表示一整块内容，没有实际的语意
- \<span> 表示行内元素，表示一行中的一小段内容，没有实际的语意
- 含样式和语意的标签
    - \<em> 标签行内元素  表示语气的强调
    - \<i> 标签行内元素 表示专业词汇
    - \<b> 标签行内元素 表示文档中的关键词或者产品名
    - \<strong> 标签行内元素
### 1.6图片标签
- \<img> 可以再网页中插入图片，常用属性
    - src 定义图片的应用地址
    - alt 定义图片加载失败时显示的文字
### 1.7链接标签
- \<a> 标签可以再网页上定义一个链接地址，常用属性
    - href 定义调整地址 
        - \# 表示页面底部 
    - title 定义鼠标悬停时弹出的提示框
    - target 定义链接窗口打开的位置
        - target="_self" 缺省值，在原来页面上打开
        - target="_blank" 会打开一个新窗口
### 1.8列表标签
- 有序列表，使用\<ol>\<li>实现,会自动加编号
    ```html
    快捷键
        ul>li*3 并加上tab
        ul>(li>a{xxx})*3 并加上tab
    <ol>
    <li>xxx</li>
    <li>xxx</li>                
    </ol>
    ```
- 无序列表，使用\<ul>\<li>实现
    ```html
    <ul>
    <li>xxx</li>
    <li>xxx</li>                
    </ul>
    ```
- 定义列表 
    - \<di> 标签表示列表的整体
    - \<dt> 标签定义术语的题目
    - \<dd> 标签是术语的解释
    - \<dl> 可以有多个题目和解释
    ```html
    快捷键 dl>(dd+dt)*3 并加上tab
    <dl>
        <dt>html</dt>
        <dd>负责页面结构</dd>
        <dt>css</dt>
        <dd>负责页面表现</dd>
        <dt>javascript</dt>
        <dd>定义页面行为</dd>
    </dl>
    ```
### 1.9表格标签
- \<table> 声明一个表格，常用属性有
    - border 定义表格边框 设置值为数值
    - cellpadding 定义单元格内容和边框的距离 设置值为数值
    - cellspacing 定义单元格和单元格之间的距离 设置值为数值
    - align 设置表格整体相对于浏览器的对齐方式
        - left
        - center
        - right
- \<tr> 定义表格中的一行
- \<td>和\<th>定义一行中的一个单元格，td表示普通单元格，th表示表头单元格
    - align 表格中内容对齐方式 
    - valign 表格中内容对齐方式 top|middle|bottom
    - colspan 设置水平合并 设置值为数值
    - rowspan 设置垂直合并 设置值为数值
    ```html
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>表练习</title>
    </head>
    <body>
        <table border="1" width="600" hight="300" cellspacing="1" cellpadding="1" align="center">
            <tr>
                <th colspan="5">个人简历</th>
            </tr>

            <tr>
                <td width="20%">姓名</td>
                <td width="20%"></td>
                <td width="20%">性别</td>
                <td width="20%"></td>
                <td rowspan="5" align="center" width="20%">
                    <img src="../images/shout.png" alt="shout">
                </td>
            </tr>
            <tr>
                <td>民族</td>
                <td></td>
                <td>出生日期</td>
                <td></td>
            </tr>
            <tr>
                <td>政治面貌</td>
                <td></td>
                <td>健康状况</td>
                <td></td>
            </tr>
            <tr>
                <td>籍贯</td>
                <td></td>
                <td>学历</td>
                <td></td>
            </tr>
            <tr>
                <td>邮箱</td>
                <td></td>
                <td>电话</td>
                <td></td>
            </tr>
        </table>
    </body>
    </html>
    ```
    ![alt](./image/table_exercise.png)
### 1.10表单
- \<form> 标签 定义整体的表单区域
    - action 属性 定义表单提交地址
    - method 属性 定义表单的提交方式 get|post
- \<label> 标签 为表单元素定义文本注释
    - for 属性  和input中的id连接起来，点击时效果较棒
- \<input> 标签 定义通用表单元素
    - type属性
        - text 定义单行文本输入框
        - password 定义密码输入框
        - radio 定义单选框
        - checkbox 定义复选框
        - file 定义上传文件
        - submit 定义提交按钮
        - reset 定义重置按钮
        - image 定义图片作为提交按钮，用src属性定义图片地址
        - hidden 定义一个隐藏表单域，通过value用来存储值
    - value 属性 定义表单的元素值(针对选择的选择项，一定要写)
    - name 属性 定义表单的元素的名称 此名称是提交数据时的键名(一定要写)
- \<textarea> 标签 用于多行输入（大文本输入）
- \<select>标签 定义下拉表单元素
- \<option>标签 与\<select>标签配合，定义下拉表单元素中的选项