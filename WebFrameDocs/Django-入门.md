### 一、视图

1. URLConf
- URL获取值
    - 请求的url被看做是一个普通的python字符串，进行匹配时不包括域名、get或post参数。
    - 在这部分中，URL设置正则即可，会传递给对应的视图函数。
    
    > 具体获取参数方式
    >  - 位置参数
    >      - 使用小括号将对应正则框柱即可
    >      - exp:`url(r'^index(\d+)/$',views.index),`
    >  - 关键字参数
    >      - 正则表达式部分为组命名
    >      - exp:`url(r'^index(?P<id1>\d+)/$',views.index),`
    >      - 注意上述例子中，index视图函数中参数名必须是`id1`


2. HttpResponse对象
- 属性
    - path：一个字符串，表示请求的页面的完整路径，不包含域名和参数部分。
    - method：一个字符串，表示请求使用的HTTP方法，常用值包括：'GET'、'POST'。
    在浏览器中给出地址发出请求采用get方式，如超链接。
    在浏览器中点击表单的提交按钮发起请求，如果表单的method设置为post则为post请求。
    - encoding：一个字符串，表示提交的数据的编码方式。
    如果为None则表示使用浏览器的默认设置，一般为utf-8。
    这个属性是可写的，可以通过修改它来修改访问表单数据使用的编码，接下来对属性的任何访问将使用新的encoding值。
    - GET：QueryDict类型对象，类似于字典，包含get请求方式的所有参数。
    - POST：QueryDict类型对象，类似于字典，包含post请求方式的所有参数。
    - FILES：一个类似于字典的对象，包含所有的上传文件。
    - COOKIES：一个标准的Python字典，包含所有的cookie，键和值都为字符串。
    - session：一个既可读又可写的类似于字典的对象，表示当前的会话，只有当Django 启用会话的支持时才可用，详细内容见"状态保持"。

- 2.1 QueryDict对象
  - 定义在django.http.QueryDict
  - HttpRequest对象的属性GET、POST都是QueryDict类型的对象
  - 与python字典不同，QueryDict类型的对象用来处理同一个键带有多个值的情况
  - 方法get()：根据键获取值
  - 如果一个键同时拥有多个值将获取最后一个值
  - 如果键不存在则返回None值，可以设置默认值进行后续处理
  - 方法getlist()：根据键获取值，值以列表返回，可以获取指定键的所有值
  - 如果键不存在则返回空列表[]，可以设置默认值进行后续处理

3. HttpResponse对象

   视图在接收请求并处理后，必须返回HttpResponse对象或子对象。在django.http模块中定义了HttpResponse对象的API。HttpRequest对象由Django创建，HttpResponse对象由开发人员创建。

- 3.1 JsonResponse
  - 在浏览器中使用javascript发起ajax请求时，返回json格式的数据，此处以jquery的get()方法为例。类JsonResponse继承自HttpResponse对象，被定义在django.http模块中，创建对象时接收字典作为参数。
    - 由于ajax请求是一个异步操作，若是需要同步操作，可以在ajax中加入`'async':flase`即可

- 3.2 HttpResponseRedirect
  - 当一个逻辑处理完成后，不需要向客户端呈现数据，而是转回到其它页面，如添加成功、修改成功、删除成功后显示数据列表，而数据的列表视图已经开发完成，此时不需要重新编写列表的代码，而是转到这个视图就可以，此时就需要模拟一个用户请求的效果，从一个视图转到另外一个视图，就称为重定向。

  - Django中提供了HttpResponseRedirect对象实现重定向功能，这个类继承自HttpResponse，被定义在django.http模块中，返回的状态码为302。



### 二、模板

模板是HTML页面，可以根据视图中传递过来的数据进行填充

1. 基本使用方式

    ```python
    from django.template import Template, Context

    text = Template("this is template, i'm {{name}}")
    content = Context({"name":"小白"})
    text.render(content)
    ```

2. 变量

  - 变量传递给模板的数据

      要遵守标识符规则, 注意一定以字母开头
      语法 {{ var }}
      注意：如果使用的变量不存在，则自动插入的是空字符串

  - 在模板中使用点语法

      点号可以访问字典的键、属性、方法或对象的索引
      字典查询
      属性或者方法
      数字索引

  - 在模板中调用对象的方法

      注意：在模板里定义的函数不能传递self以外的参数

  - 上述三种方式举例

      ```python
      from django.template import Template, Context
      # 使用变量传递
      text = Template("this is template, i'm {{name}}")
      content = Context({"name":"小白"})
      text.render(content)
          
      # 使用点语法
      pc_info_dict = {"cpu":"i3", "disk":"东芝", "display":"apple"}
      pc_info_list = ["i3", '东芝']
      class PersonComputer:
          def __init__(self):
              self.cpu = 'i3'
              self.disk = '东芝'
              self.display = "apple"
          
      # 字典
      text = Template("pc have {{info.cpu}} cpu, {{info.disk}} disk")
      content = Context({"info": pc_info_dict})
      text.render(content)
          
      # 列表
      text = Template("pc have {{info.0}} cpu, {{info.1}} disk")
      content = Context({"info": pc_info_list})
      text.render(content)
          
      # 对象
      text = Template("pc have {{info.cpu}} cpu, {{info.disk}} disk")
      content = Context({"info": PersonComputer()})
      text.render(content)
      ```

3. 标签

  - 3.1 if 标签
      - 计算变量的值，如果为真（即存在、不为空，不是假值）

      - 支持使用and、or 或not 测试多个变量，或者取反指定的变量

      - 注意：上述的and、or 或not不允许使用(),真遇到了，可以使用嵌套结构
      - 格式1

              {% if %}
                  内容
              {% endif %}
      - 格式2

              {% if %}
                  内容
              {% else %}
                  内容
              {% endif %}
      - 格式3

              {% if %}
                  内容
              {% elif %}
                  内容
              {% elif %}
                  内容
              ...
              {% else %}
                  内容
              {% endif %}

  - 3.2 for 标签
      - 用于迭代序列中的各个元素

      - 格式1

              {% for 变量 in Python对象 %}
                  语句
              {% endfor %}
      - 格式2

              {% for 变量 in Python对象 %}
                  语句
              {% empty %}  # 注意：列表为空或者列表不存在时执行empty内的内容
                  语句2
              {% endfor %}
      - 格式3

              {{ forloop.counter }}

  - 3.3 ifequal/ifnotequal 标签
      - 标签比较两个值，如果相等/不相等，显示内部的内容
      - 本质上可以使用if 和 ==/!= 来替代
      - 格式

              {% ifequal user currentuser %}
                  内容
              {% endifequal %}

  - 3.4 注释
      - 用来注释代码，让其不显示
      - 注释不可以嵌套

      - 单行注释：

              {# 被注释的内容 #}
      - 多行注释

              {% comment %}
                  注释内容
              {% endcomment %}

  - 3.5 include 
      - 加载模板并以标签内的参数渲染
      - 格式：

              {% include '模板目录' 参数1 参数2 %}

4. 过滤器

  模板过滤器是在显示变量之前调整变量值的简单方式。过滤器使用管道符号指定

  - 基本格式

    语法 {{ var|过滤器 }}

  - 示例：

    - 过滤器可以传递参数，参数用引号引起来
      `join 格式 列表|join:"#"`
      示例：{{list1|join:"#"}}
    - 如果一个变量没有被提供，或者值为false,空，我们可以通过 default 语法使用默认值
      格式： {{str1|default:"没有"}}
      根据给定格式转换日期为字符串：date
      格式： {{dateVal|date:'y-m-d'}}
      HTML转义：escape
    - 问题：return render(request, 'myApp/index.html', {"code": "`<h1>sunck is a very good man</h1>`"})中的{{code}}
      {{code}}里的code被当作`<h1>sunck is a very good man</h1>`显示，未经过渲染
      解决方法：
      {{code|safe}}
      或  {% autoescape off %}
      {{code}}
      {% endautoescape %}  # 这个可以一口气解决一堆
    
5. 模板

  - 模板继承可以减少页面的重复定义，实现页面的重用

  - block标签：在父模板中预留区域 ，子模板去填充

  - 语法 ： 

    {% block 标签名 %}

    {% endblock 标签名 %}
    
  - extends标签：继承模板，需要写在模板文件的第一行

  - 语法 ： 

    {% extends 'myApp/base.html' %}
    {% block main %}
    内容
    {% endblock 标签名 %}

    - 示例：
    ```markdown
    定义父模板
        body标签中
        {% block main %}
    
        {% endblock main %}
    
        {% block main2 %}
    
        {% endblock main2 %}
    定义子模板
        {% extends 'myApp/base.html' %}
        {% block main %}
        <h1>sunck is a good man</h1>
        {% endblock main %}
    
        {% block main2 %}
        <h1>kaige is a good man</h1>
        {% endblock main2 %}
    ```

  - include

    作用：加载模板并以标签内的参数渲染
    格式：{% include '模板目录' 参数1 参数2 %}

6. 反向解析

  - 在模板中需要将href设置为`{% url "namespace:name" %}`
  ```markdown
  在模板文件中使用时，格式如下:
  {% url 'namespace名字：name' %} 例如{% url 'booktest:fan2'%}
  带位置参数：
  {% url 'namespace名字：name' 参数 %} 例如{% url 'booktest:fan2' 1%}
  带关键字参数：
  {% url 'namespace名字：name' 关键字参数 %} 例如{% url 'booktest:fan2' id=1 %}
  ```
  - 在视图中的操作
  ```markdown
  在重定向的时候使用反向解析：
  from django.core.urlresolvers import reverse
  无参数：
  reverse('namespace名字:name名字')
  如果有位置参数
  reverse('namespace名字:name名字', args = 位置参数元组)
  如果有关键字参数
  reverse('namespace名字:name名字', kwargs=字典)
  ```



### 三、模型
1. 字段查询
       此查询类似于SQL中的select查询

- 1.1 查询集
  - all() 返回所有结果
  - filter(条件) 返回满足条件的内容
  - exclude(条件) 返回满足条件之外的内容
  - order_by(字段) 根据字段进行排序

- 2.2 返回单个值的过滤器
  - get() 返回单个值
  - count() 返回查询集中的内容个数
  - aggregate() 聚合
- 2.3 返回某个查询集中内容是否存在
  - exists() 返回内容是否存在

2. 条件查询

- exact 判断相等
```python
模型名.objects.filter(pk__exact=1)
或者
模型名.objects.filter(pk=1)
```

- contains 包含xx内容
```python
模型名.objects.filter(字段名__contains="xx")
```

- endswith及startswith 结束和开头包含xx
```python
模型名.objects.filter(字段名__startswith="xx")
模型名.objects.filter(字段名__endswith="xx")
```

- isnull 内容是否为空


- in 内容是否在范围以内


- 比较查询

    - gt 大于
    - gte 大于等于
    - lt 小于
    - lte：小于等于
    
- 日期查询

    - year 年
    - month 月
    - day 天
    - week_day 
    - hour
    - minute
    - second
    
- F对象
    - 用于属性和属性的比较,同时F对象可以参加运算
  ```python
  # 查询阅读量大于等于评论量的图书
  from django.db.models import F
  Book.objects.filter(readnum_gte = F('commentnum'))
  # 查询阅读量大于等于2倍的评论量的图书
  Book.objects.filter(readnum_gte = F('commentnum')*2)
  ```
- Q对象
  - 多个过滤器逐个调用表示逻辑与关系
    - Q对象可以使用&、|连接，&表示逻辑与，|表示逻辑或。
    - Q对象前可以使用~操作符，表示非not。
  ```python
  from django.db.models import Q
  # 查询阅读量大于20，或编号小于3的图书，只能使用Q对象实现
  Book.objects.filter(Q(readnum__gt = 20) | Q(readno__lt = 3))
  ```

- aggregate 聚合
  - 返回值是字典类型
    - {'聚合类小写__属性名':值}
    ```python
    from django.db.models import Sum, Avg, Count, Max, Min
    # 统计Book中title的数量，  下面聚合结果为{'title__count': 2}
    Book.objects.aggregate(Count("title"))
    ```

4. 关联查询（类似于SQL中的join）
- 一对多查询
  - 使用对象查询
    - 一对应的对象名.多对应的模型名小写_set.all()
    ```python
    obj = 一模型名.objects.filter(pk=1)
    obj.多模型名_set.all()
    ```
  - 使用类查询
    - 一模型名关联属性名__-模型类属性名=条件
    ```python
    # 多模型名.objects.filter(多模型中对应一模型的字段__-模型类属性名="图灵出版社")
    # 查询图灵出版社所有图书
    Book.objects.filter(publisher__name='图灵出版社')
    ```
  
- 多对一查询
  - 使用对象查询
    - 多对应对象名.多对应的模型类中关系类的属性
    ```python
    obj = 多模型名.objects.filter(pk=1)
    obj.对应属性名
    ```
  - 使用类查询
    - 关联模型类名小写__属性名__条件运算符=条件
    ```python
    一模型名.objects.filter(关联模型类名小写__属性名="天龙八部")
    # 查询天龙八部对应的出版社
    Publisher.objects.filter(book__title="天龙八部")
    ```
    
5. 元选项
- 在模型类中定义类Meta，用于设置元信息，如使用db_table自定义表的名字。
  ```python
  class Meta:
      db_table = "bookinfo" # 定义表名
  ```

6. 模型管理器

> 属性objects：管理器，是models.Manager类型的对象，用于与数据库进行交互。
>
> 当没有为模型类定义管理器时，Django会为每一个模型类生成一个名为objects的管理器，自定义管理器后，Django不再生成默认管理器objects。
>
> 使用方式
> 1. 创建模型管理器类
> 2. 使用时，需要在对应类中加入模型管理器的实例化对象

- 自定义管理器类主要用于两种情况：
  - 1.修改原始查询集，重写all()方法
  - 2.向管理器类中添加额外的方法，如向数据库中插入数据。

7. 获取模型中对象的属性值
- 获取对应字段的对象
    - 模型类._meta.get_field(对应字段)
- 获取对应字段的值
  - 模型类._meta.get_field(对应字段).verbose_name
  
  ```python
  class UserInfo(models.Model):
      """用户信息表"""
      username = models.CharField(max_length=32, verbose_name="用户名")  
      email = models.EmailField(max_length=32, verbose_name="邮箱")
      mobile_phone = models.CharField(max_length=32, verbose_name="手机号")
      password = models.CharField(max_length=32, verbose_name="密码")
  
  # 若需要获取到email的详细值可以使用
  email_obj = UserInfo._meta.get_field('email')
  email_obj.verbose_name
  ```
- 若是需要通过字段查询对应的模型类，一般方式有
    - 当前字段是这个类的
        - 字段对象.model , 例如`email_obj.model`
    - 当前这个字段是这个类的外键
        - 字段对象.remote_field.model  例如`email_obj.remote_field.model`

### 四、admin
1. 注册模型，实现显示 
  ```python
  from django.contrib import admin
  from book.models import Author
  
  admin.site.register(Author)
  ```

2. 管理页显示
  - 使用管理类实现

    - 使用注册参数
    - 使用装饰器

    ```python
    from django.contrib import admin
    from book.models import Author
    
    # 装饰器
    @admin.register(Author)
    class AuthorAdmin(admin.ModelAdmin):
        pass
    
    # 注册参数
    class AuthorAdmin(admin.ModelAdmin):
        pass
    admin.site.register(Author, AuthorAdmin)
    ```
  - 控制管理页关键字段
      - list_display 列表中的列
          - 添上对应模型中的类属性即可
          - 类字段修改列名,只要在定义时加入`verbose_name`字段即可
          - 将类中的方法作为列（不可以排序）
              - 直接写方法名即可
              - 想要让方法可以排序需要在模型中将方法名设定为对应字段`方法名.admin_order_field='模型类字段'`
              - 想要修改列名`方法名.short_description=名称`
      - list_per_page 设定每页显示数据量的多少
      - list_filter 右侧过滤器
      - search_fields 查询字段
      - actions_on_top 操作选项的位置--上
      - actions_on_bottom 操作选项位置--下

  - 编辑管理页关键字段
      - 注意field和fieldset只能单独使用
      - field 显示字段顺序
      - fieldset 分组显示

      ```python
          fields = ['last_name', 'first_name', 'email']
          fieldsets = (
              ('姓氏', {'fields': ['first_name']}),
              ('名称', {'fields': ['last_name']})
          )
      ```
      - 关联对象
        - 在一对多的关系中，可以在一端编辑页面修改多段的内容。将多端的内容嵌入到一段中有两种方式[表格、块]
        - 使用时需要创建一个多端的表格或者块形式的类，并将其在一端中使用

      ```python
      from django.contrib import admin
      from book.models import Book, Publisher
      # 创建块
      class BookStackedInline(admin.StackedInline):
          model = Book
          extra = 2
      # 创建表格
      class BookTabularInline(admin.TabularInline):
          model = Book
          extra = 2
      
      @admin.register(Publisher)
      class PublisherAdmin(admin.ModelAdmin):
          # 使用块方式
          inlines = [BookStackedInline]
          # 使用表格
          inlines = [BookTabularInline]
      ```
