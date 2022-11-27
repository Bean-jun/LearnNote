### 1. 风格

*   GET 获取内容
*   POST 增加内容
*   PUT 修改内容
*   DELETE 删除内容
*   PATCH(UPDATE)        在服务器上更新资源
*   OPTIONS 获取信息，源于资源的那些属性是客户端可以改变的

#### 1.1 域名

*   应该尽量将API部署在专用域名下
    `https://api.---.com`
*   若是确定API很简单，不会有扩展，可以考虑放在主域名下
    `https://www.---.com/api`

#### 1.2 版本

*   应该将API版本放在URL中
*   或者放入将版本号放在请求头中

#### 1.3 路径

*   资源作为网址，只能用名词，不能用动词，而且所用名词一般和数据库表名对应
*   API中的名词应该使用复数。无论子资源或者所有资源

#### 1.4 过滤信息

*   ?limit=10 指定返回记录的数据
*   ?offset=10 指定返回数据点开始位置 ...

#### 1.5 状态码

*   200 成功
*   201 新建或者修改成功 ...

#### 1.6 错误处理

*   对于状态码不正常的情况，服务器一般需要向指定用户返回出错信息

#### 1.7 返回结果

*   返回请求结果

#### 1.8 超媒体

*   在返回结果中提供链接，使得用户不查文档也知道下一步做什么

#### 1.9 其他

*   一般返回json结果，不要返回xml

### 2. 序列化和反序列化

*   序列化 -- 用的较多

    将模型转换为字典为序列化

*   反序列化 -- 一般都在修改put和新增post

    将字典转换为模型

```python
from django.db import models
from django.views.generic import View
from django.http import JsonResponse
from rest_framework import serializers


# models文件
class Author(models.Model):
    """图书作者"""
    first_name = models.CharField(verbose_name="姓氏", max_length=30)
    last_name = models.CharField(verbose_name="名称", max_length=40)
    email = models.EmailField(verbose_name="邮箱")

    def __str__(self):
        return self.first_name


class Book(models.Model):
    """图书"""
    author = models.ForeignKey(to='Author', on_delete=models.CASCADE, verbose_name="作者")
    title = models.CharField(max_length=30)
    publication_date = models.DateTimeField(auto_now_add=True)


# serializer文件
class AuthorSerializer(serializers.ModelSerializer):
    """author序列化器"""

    class Meta:
        model = Author
        fields = "__all__"
        # 对字段进行功能扩展--修改选项参数
        extra_kwargs = {
            # xxxxx
        }


class BookSerializer(serializers.ModelSerializer):
    """Book序列化器"""

    # author = serializers.StringRelatedField()  # 将关联对象的__str__方法返回
    # author = serializers.PrimaryKeyRelatedField() # 设置关联对象主键
    # author = AuthorSerializer() # 直接将author对象序列化过来哦--注意：一对多时需要加入many=True

    class Meta:
        model = Book
        fields = "__all__"

    # 反序列化验证--类似forms验证，但也有些许不同

    # 单一校验某一个字段
    def validate_title(self, value):
        # value指前端传递过来的数据，校验之后直接返回即可

        return value

    # 对所有字段进行校验，attrs【字典】中包含了所有传递过来的字段
    def validate(self, attrs):
        return attrs

    # 对于继承ModelSerializer的类而言，不需要自己实现create及update方式
    # # 将反序列化的数据进行创建
    # def create(self, validated_data):
    #     '''保存数据'''
    #     book = Book.objects.create(**validated_data)
    #     return book
    # 
    # # 将反序列化的数据进行修改
    # def update(self, instance, validated_data):
    #     '''修改数据'''
    #     instance.update(**validated_data)
    #     instance.save()

    #     return instance


# views文件
class BookListView(View):
    """获取全部数据&增加一条数据"""

    def get(self, request):
        '''获取全部数据--序列化'''
        book = Book.objects.all()
        serializer = BookSerializer(instance=book, many=True)
        # serializer.data 就是序列化之后的json格式内容
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        '''反序列化'''
        pass
```

#### 2.1 在开发rest api的视图中，每一个视图操作的数据不同，但是基本套路相同

    增加

      校验数据 --》 执行反序列化 --》保存数据 --》将保存的对象序列化并返回

    删除

      判断内容是否存在 --》 执行数据库删除

    修改

      判断是否存在 --》 校验请求数据 --》执行反序列化 --》 保存数据 --》 将保存的对象序列化并返回

    查询

      查询数据库 --》 数据序列化

### 3. 视图

#### 3.1 Request和Response

*   Request 在原django框架的基础上添加了Parse解析器，用来解析请求过来的数据
    *   常用属性
    ```markdown
    返回请求体数据 

    1. data 
       
        包含了POST PUT PATCH请求过来的数据

    2. query_params 
        
        包含了GET请求过来的数据
    ```

*   Response

    *   使用部分
        `rest_framework.response.Response`

    ```markdown
    Response(data=None, status=None,
                template_name=None, headers=None,
                exception=False, content_type=None)

    data=None,      # 序列化之后的数据
    status=None,    # 状态码
    template_name=None,     # 模板名称
    headers=None,   # 响应头
    exception=False, 
    content_type=None   # 响应数据的content-type
    ```

    *   常用属性

    ```markdown
    1. data 未处理化的数据

    2. content 通过render处理之后返回前端的数据
    ```

#### 3.2 APIView

*   使用部分

    `rest_framework.view.APIView`

*   介绍

    APIView 和View 的不同在于，APIView对原View中的request进行了进一步的封装

*   使用

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from book_drf.models import Book
from book_drf.serializer import BookSerializer


class BookListAPIView(APIView):
    """获取全部数据&增加数据"""

    def get(self, request):
        '''获取全部数据'''
        book = Book.objects.all()
        serializer = BookSerializer(instance=book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''添加数据'''
        res = request.data
        serializer = BookSerializer(data=res)
        if serializer.is_valid(raise_exception=True):
            # 校验成功  开始反序列化
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookDetailAPIView(APIView):
    """获取单条数据&修改单条数据&删除单条数据"""

    def get(self, request, pk):
        '''查询单一数据'''
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(instance=book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        '''修改数据'''
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        res = request.data
        serializer = BookSerializer(instance=book, data=res)
        if serializer.is_valid(raise_exception=True):
            # 校验成功  开始反序列化
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        '''删除数据'''
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        book.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
```

#### 3.3 GenericAPIView

*   使用部分

    `rest_framework.generics.GenericAPIView`

*   介绍

    GenericAPIView继承至APIView,增加了操作序列化器和数据查询的方法

*   提供关于序列化器的属性和方法
    *   属性
        *   serializer\_class 指明视图使用那个序列化器
    *   方法
        *   get\_serializer\_class(self)  返回序列化器类
        *   get\_serializer(self,\*args,\*\*kwargs) 返回序列化器对象，主要提供给Mixin扩展类使用

*   提供数据库查询的属性和方法
    *   属性
        *   queryset 指明数据库的查询集
    *   方法
        *   get\_queryset(self) 返回视图使用的查询集
        *   get\_object(self) 返回详情视图所需要的模型类数据对象

*   其他属性
    *   pagination\_class 指明分页控制类
    *   filter\_backends 指明控制过滤后端

*   使用

```python
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from book_drf.models import Book
from book_drf.serializer import BookSerializer


class BookListGenericAPIView(GenericAPIView):
    """使用GenericAPIView实现  获取全部数据&增加数据"""
    queryset = Book.objects.all()  # 指定查询集
    serializer_class = BookSerializer  # 指定序列化器

    def get(self, request):
        book = self.get_queryset()  # 获取查询集
        serializer = self.get_serializer(book, many=True)  # 将查询集序列化
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)  # 将查询集序列化
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class BookDetailGenericAPIView(GenericAPIView):
    """使用GenericAPIView实现  获取单条数据&修改单条数据&删除单条数据"""
    queryset = Book.objects.all()  # 指定查询集
    serializer_class = BookSerializer  # 指定序列化器

    def get(self, request, pk):
        book = self.get_object()  # 获取pk对应的结果
        serializer = self.get_serializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        '''修改一条数据'''
        book = self.get_object()
        serializer = self.get_serializer(instance=book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
```

#### 3.4 Mixin 混入GenericAPIView

*   介绍

    简化get、post....中的代码

*   使用

```python
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
)
from rest_framework.generics import GenericAPIView
from book_drf.models import Book
from book_drf.serializer import BookSerializer


class BookListGenericAPIViewMixin(ListModelMixin, CreateModelMixin, GenericAPIView):
    """GenericAPIView混合Mixin使用"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request):
        return self.list(request)  # 调用父类方式显示查询集的返回

    def post(self, request):
        return self.create(request)


class BookDetailGenericAPIViewMixin(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """GenericAPIView混合Mixin使用"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
```

#### 3.5 关于rest\_framework.generics中的其他类

`CreateAPIView` `RetrieveModelMixin` 等等，他们继承于Minix及GenericAPIView类，在使用时可以进一步简化代码,可以简化简化get、post....之类的实例方法

#### 3.6 视图集 viewsets 修改了View的as\_view方法，将序列化全部和序列化一个内容糅合在一起，实现代码的简化

*   ViewSet 继承APIView

    *   代码演示

```python
# url部分
from django.urls import path
from book_drf import views

# 由于查询都写在一个类中，所以需要在路由分发中将其隔开
path('books_ViewSet/', views.BookViewSet.as_view({'get': 'list'})),
path('books_ViewSet/<int:pk>/', views.BookViewSet.as_view({'get': 'retrieve'})),

# views部分
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from book_drf.models import Book
from book_drf.serializer import BookSerializer


class BookViewSet(ViewSet):
    """使用ViewSet视图集实现查询全部和查单一"""

    def list(self, request):
        '''查全部数据'''
        book = Book.objects.all()
        serializer = BookSerializer(instance=book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        '''查单一数据'''
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
```

*   GenericViewSet 继承GenericAPIView
    *   代码演示

```python
# url部分
from django.urls import path
from book_drf import views

# GenericViewSet使用
path('books_GenericViewSet/', views.BookGenericViewSet.as_view({'get': 'list'})),
path('books_GenericViewSet/<int:pk>/', views.BookGenericViewSet.as_view({'get': 'retrieve'})),

# views部分
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from book_drf.models import Book
from book_drf.serializer import BookSerializer


# class BookGenericViewSet(ReadOnlyModelViewSet, GenericViewSet):
class BookGenericViewSet(ReadOnlyModelViewSet):
    """使用GenericViewSet视图集实现查询全部和查单一"""
    # ReadOnlyModelViewSet 继承了GenericViewSet类
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

*   ModelViewSet 由于继承GenericAPIView和mixins中的大部分类，在使用时，直接设置查询集合序列化器即可

#### 3.7 路由设置【只能结合视图集使用】

*   介绍

    在刚刚的设置中，as\_view需要在其中设置分发逻辑，这部分可以直接简化

*   代码

```python
# 路由这部分关于as_view部分写着较为麻烦，可以直接配置路由即可
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()  # 创建路由
# router.register('路由匹配', views.类视图)  # 注册路由
# urlpatterns += router.urls  # 添加路由
```

*   注意点

    使用路由时，对于类视图中单独定义`其他`的接口（抛开最基本的 增删查改的五条）是没办法设置到的，此时需要 设置路由

    *   方式一：
        *   直接在urls中写，比如 `path('books_GenericViewSet/last', views.BookGenericViewSet.as_view({'get': 'last'}))`
    *   方式二：
        *   在类方法中添加装饰器即可

```python
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from book_drf.models import Book
from book_drf.serializer import BookSerializer


class BookModelViewSet(ModelViewSet):
    """ModelViewSet实现增删查改"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    from rest_framework.decorators import action

    # 将生成路由为BookModelViewSet/last/
    @action(methods=['get'], detail=False)  # detail设置为False表示当前请求不需要pk,即id
    # 若是将detail设置为True后将生成路由为BookModelViewSet/pk/last/
    def last(self, request):
        '''查最后一本书'''
        book = self.get_queryset().last()
        return Response(self.get_serializer(book).data, status=status.HTTP_200_OK)
```

### 4. 认证【指针对继承了APIView的视图】

*   认证流程

```markdown
当用户发来请求时，找到认证的所有类并实例化成为对象列表，然后将对象列表封装到新的request对象中。

以后在视同中调用request.user

在内部会循环认证的对象列表，并执行每个对象的authenticate方法，该方法用于认证，他会返回两个值分别会赋值给
request.user/request.auth 
```

*   全局认证【可以使用 DEFAULT\_AUTHENTICATION\_CLASSES 设置全局的默认身份验证方案】

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}
```

*   局部认证 【针对单一视图进行认证】

```python
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView


class ExpAPIView(APIView):
    """认证样例"""
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    # .......
```

*   认证失败返回值

    当未经身份验证的请求被拒绝时，有下面两种不同的错误代码可使用。

        HTTP 401 未认证
        HTTP 403 无权限

### 5. 权限

*   类别

```markdown
AllowAny

权限类将允许不受限制的访问，而不管该请求是否已通过身份验证或未经身份验证。 此权限不是严格要求的，因为你可以通过使用空列表或元组进行权限设置来获得相同的结果，但你可能会发现指定此类很有用，因为它使意图更明确。

IsAuthenticated

权限类将拒绝任何未经身份验证的用户的权限，并允许其他权限。 如果你希望你的API仅供注册用户访问，则此权限适用。 如果你希望你的API允许匿名用户读取权限，并且只允许对已通过身份验证的用户进行写入权限，则此权限是适合的。

IsAdminUser

除非user.is_staff为True，否则IsAdminUser权限类将拒绝任何用户的权限，在这种情况下将允许权限。 如果你希望你的API只能被部分受信任的管理员访问，则此权限是适合的。

IsAuthenticatedOrReadOnly

将允许经过身份验证的用户执行任何请求。只有当请求方法是“安全”方法（GET, HEAD 或 OPTIONS）之一时，才允许未经授权的用户请求。
如果你希望你的API允许匿名用户读取权限，并且只允许对已通过身份验证的用户进行写入权限，则此权限是适合的。

```

*   全局使用 【不推荐】【默认权限策略可以使用DEFAULT\_PERMISSION\_CLASSES设置进行全局设置】

```python
REST_FRAMEWORK = {
    # 权限部分
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
```

*   局部使用

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class ExpAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    # .......
```

*   自定义权限

重写BasePermission并实现以下方法中的一个或两个

    .has_permission(self, request, view)  是否可以访问视图 

    .has_object_permission(self, request,
    view, obj)  是否可以访问数据对象

使用时需要自定义权限类，继承于BasePermission，然后重写上面的方式，最后给到permission\_classes即可

```python
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        # xxxxxx
        return  # 想要返回的内容

    def has_object_permission(self, request, view, obj):
        # xxxxxx
        return  # 想要返回的内容


class ExpAPIView(APIView):
    permission_classes = (MyPermission,)
    # .......
```

### 6. 限流 【减少接口访问的频次】

[限流官方-link](https://www.django-rest-framework.org/api-guide/throttling/)

*   全局

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [  # 配置全局限流方式
        'rest_framework.throttling.AnonRateThrottle',  # 匿名用户
        'rest_framework.throttling.UserRateThrottle'  # 登录用户
    ],
    'DEFAULT_THROTTLE_RATES': {  # 限制频次
        'anon': '100/day',  # 一天100次
        'user': '1000/day'  # 一天1000次
    }
}
```

### 7. 过滤&排序

安装依赖`pip install django-filter`

*   使用

```markdown
1. 注册django_filter
2. 配置 REST_FRAMEWORK = {
   'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
   }
3. 过滤字段
from django_filters.rest_framework import DjangoFilterBackend
filter_backends = [DjangoFilterBackend]
filter_fields = ['title', 'id']     # 针对某一字段过滤

4. 排序字段
from rest_framework.filters import OrderingFilter
filter_backends = [OrderingFilter]
ordering_fields = ['id']    # 针对某一字段排序
   
5. 即可以过滤，还可以排序
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
filter_backends = [DjangoFilterBackend, OrderingFilter]
filter_fields = ['id']
ordering_fields = ['id']
```

### 8. 分页

*   全局

```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}
```

*   使用

```python
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from book_drf.models import Book
from book_drf.serializer import BookSerializer


class LargeResultsSetPagination(PageNumberPagination):
    """自定义分页"""
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 4
    
    
class BookModelViewSet(ModelViewSet):
    """ModelViewSet实现增删查改"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = LargeResultsSetPagination    # 将自定义分页加入即可
    
# PageNumberPagination  分页控制
# LimitOffsetPagination 偏移控制
```

### 9. 版本

```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning'
}
```

### 10. 异常

[参考](https://www.django-rest-framework.org/api-guide/exceptions/)

### 11. 接口文档

*   安装依赖
    `pip install coreapi`

*   配置

```python
# setting文件
REST_FRAMEWORK = {
        'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}
# urls 文件
from django.urls import path
from rest_framework.documentation import include_docs_urls

path('docs/', include_docs_urls(title='测试接口文档')),
```
