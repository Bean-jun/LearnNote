### 一、视图

1. FBV 和CBV写法简介

```python
from flask import Flask, views

app = Flask(__name__)


def auth(func):
    def inner(*args, **kwargs):
        print('before')
        result = func(*args, **kwargs)
        print('after')
        return result

    return inner


@app.route('/', methods=['GET'], endpoint='index_1')
@auth
def index():
    """自定义页"""
    return "hello"


class IndexView(views.View):
    methods = ['GET']
    decorators = [auth, ]

    def dispatch_request(self):
        print('Index')
        return 'Index!'


app.add_url_rule('/index', view_func=IndexView.as_view(name='index'))  # name=endpoint


# 或者继承自MethodView，调用写好的dispatch_request


class IndexView(views.MethodView):
    methods = ['GET']
    decorators = [auth, ]

    def get(self):
        return 'Index.GET'

    def post(self):
        return 'Index.POST'


app.add_url_rule('/index', view_func=IndexView.as_view(name='index'))  # name=endpoint
```

2. request及response内容

```markdown
# 请求相关信息

# request.method

# request.args 和 django的request.GET相同

# request.form 和 django的request.POST相同

# request.values

# request.cookies

# request.headers

# request.path

# request.full_path

# request.script_root

# request.url

# request.base_url

# request.url_root

# request.host_url

# request.host

# request.files

# obj = request.files['the_file_name']

# obj.save('/var/www/uploads/' + secure_filename(f.filename))

# 响应相关信息

# return "字符串"

# return render_template('html模板路径',**{})

# response = make_response(render_template('index.html'))

# response是flask.wrappers.Response类型

# response.delete_cookie('key')

# response.set_cookie('key', 'value')

# response.headers['X-Something'] = 'A value'

# return response
```

3. session

`from flask import session`

4. 常见装饰器

- before_first_request：在处理第一个请求前运行。
- before_request：在每次请求前运行。
- after_request：如果没有未处理的异常抛出，在每次请求后运行。
- teardown_request：在每次请求后运行，即使有未处理的异常抛出。

```python
from flask import Flask, url_for, render_template, redirect, session, request

app = Flask(__name__, template_folder='templates')

# 黑名单
BLACK_LIST = ['127.0.0.2']


@app.before_request  # 在每次请求之前都会运行
def check_login():
    '''
    检测用户登录
    :return: None 表示通过，否则表示不通过
    '''
    if request.remote_addr in BLACK_LIST:
        return "你小子滚犊子"

    if request.path == url_for('login'):
        return None

    user = session.get('user_id')
    if not user:
        print("用户未登录")
        return redirect(url_for('login'))
    else:
        print("检测到用户登录，跳转到首页")
        return None


@app.after_request  # 在每次请求后运行
def check_response(response):
    '''
    返回给用户的最后一个环节
    :return:
    '''
    print("响应下")
    return response


@app.route('/login/', methods=['GET'], endpoint='login')
def login():
    session['user_id'] = 123
    return "登录成功"


@app.route('/', methods=['GET'], endpoint='index')
def index():
    return render_template('V3.html', **({'age': 12}))
```

5. 闪现

- 一般用于消息提醒，用于访问某个视图时进行设置并获取
- 这部分可以基于session实现，但是也可以直接使用flask内部提供的flash及get_flashed_messaged实现

```python
from flask import Flask, flash, get_flashed_messages

app = Flask(__name__, template_folder='templates')
app.config.from_object('settings.DevelopmentConfig')


@app.route('/login/', methods=['GET'], endpoint='login')
def login():
    flash("你好哦， 这是闪现")
    return "登录成功"


@app.route('/', methods=['GET'], endpoint='index')
def index():
    data = get_flashed_messages()
    return 'index' + str(data)


if __name__ == "__main__":
    app.run()
```

5. 中间件

- 针对app的wsgi做操作
- 使用在处理请求之前 【在before_request之前】

```python
from flask import Flask

app = Flask(__name__)


class Middleware:
    def __init__(self, old_wsgi):
        self.old_wsgi = old_wsgi

    def __call__(self, *args, **kwargs):
        # 请求之前
        return self.old_wsgi(*args, **kwargs)


if __name__ == "__main__":
    # 将原生wsgi经过Middleware中间件加工
    app.wsgi_app = Middleware(app.wsgi_app)

    app.run()
```

7. 蓝图

- 做目录划分
- 做路由前缀
- 针对某一类视图函数添加之前及之后的操作【before_request及after_request等】

```python
'''
.
├── manage.py   启动文件
└── mysite_flask    项目
    ├── __init__.py
    ├── static  静态文件
    ├── templates   模板文件
    └── views   视图模块
        ├── account.py
        └── admin.py
        
manage.py[老板] --> mysite_flask.__init__.py[经理] --> mysite_flask.views.***[打工人]
'''

# manage.py
from mysite_flask import app

if __name__ == '__main__':
    app.run()

# mysite_flask.__init__.py
from flask import Flask
from .views import account, admin

app = Flask(__name__)

# 将蓝图对象进行关联
app.register_blueprint(account.account, url_prefix='/account')  # url_prefix 路由前缀，可以在这部分加，也可以单独写在视图函数中
app.register_blueprint(admin.admin)

# mysite_flask.views.account
from flask import Blueprint

account = Blueprint('account', __name__)


@account.route('/register/')
def register():
    return "用户注册"


@account.route('/login/')
def login():
    return "用户登录"


# mysite_flask.views.admin
from flask import Blueprint

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.before_request
def before():
    print("针对单个蓝图[这里仅仅是admin]进行处理")


@admin.route('/center')
def center():
    return "用户管理后台"
```

### 二、模板

由于这部分主要使用Jinja2，且和django template非常相似，故不再重点介绍

- 自定义模板

```python
# 定义后可以在所有的模板中使用该标签
@app.template_global()
def add(value):
    return value * 2


# 定义后可以在所有的模板中使用该过滤器
@app.template_filter()
def db(a1, a2, a3):
    return a1 + a2 + a3
```

### 三、路由

1. 简单路由部分

```python
from flask import Flask

app = Flask(__name__)


# 使用装饰器添加路由 -- 推荐
@app.route('/', methods=['GET'])
def index():
    return "hello flask"


def hello():
    return "hello flask"


# 直接添加 -- 不推荐
app.add_url_rule('/hello/', view_func=hello)
```

2. 反向解析

- 和django中reverse相互类似
- 在这里一般要配合end_point【它是用来起别名的，不写默认就是函数名】使用

```python
from flask import Flask, url_for

app = Flask(__name__)


@app.route('/', methods=['GET'], endpoint='index_1')
def index():
    return "index"


@app.route('/look/', methods=['GET'])
def look():
    print(url_for('index_1'))  # 解析地址
    return 'look'
```

3. 重定向

`from flask import redirect`

4. 自定义路由

- string: (缺省值)接受任何不包含斜杠的文本
- int: 接受正整数
- float: 接受正浮点数
- path: 类似 string ，但可以包含斜杠
- uuid: 接受 UUID 字符串

```python
from flask import Flask

app = Flask(__name__)


@app.route('/url_custom/<int:fid>/', methods=['GET'])
def url_custom(fid):
    print(fid)
    return 'url_custom'
```

5. 自定义路由转换器

```python
from flask import Flask
from werkzeug.routing import BaseConverter

app = Flask(__name__)


class RegexConverter(BaseConverter):
    """自定义路由转换器"""

    def __init__(self, map, regex):
        super().__init__(map)
        self.regex = regex

    def to_python(self, value):
        '''
        匹配路由成功之后，将匹配成功后传递给视图函数中参数的值
        :param value:
        :return:
        '''
        return value

    def to_url(self, value):
        '''
        使用url_for反向生成url时，传递的参数经过改方式处理，返回值用于生成URL中的参数
        :param value: 
        :return: 
        '''
        return super(RegexConverter, self).to_url(value)


# 将自定义路由转换机加入到项目中
app.url_map.converters['xxx'] = RegexConverter


# 使用
@app.route('/<xxx("\d+"):fid>')
def index(fid):
    print(fid)
    return "hahahah"
```

### 四、信号

Flask框架中的信号基于blinker，其主要就是让开发者可是在flask请求过程中定制一些用户行为。

`pip install blinker`

1. 内置信号

```python
request_started = _signals.signal('request-started')  # 请求到来前执行
request_finished = _signals.signal('request-finished')  # 请求结束后执行

before_render_template = _signals.signal('before-render-template')  # 模板渲染前执行
template_rendered = _signals.signal('template-rendered')  # 模板渲染后执行

got_request_exception = _signals.signal('got-request-exception')  # 请求执行出现异常时执行

request_tearing_down = _signals.signal('request-tearing-down')  # 请求执行完毕后自动执行（无论成功与否）
appcontext_tearing_down = _signals.signal('appcontext-tearing-down')  # 应用上下文执行完毕后自动执行（无论成功与否）

appcontext_pushed = _signals.signal('appcontext-pushed')  # 应用上下文push时执行
appcontext_popped = _signals.signal('appcontext-popped')  # 应用上下文pop时执行
message_flashed = _signals.signal('message-flashed')  # 调用flask在其中添加数据时，自动触发
```

2. 自定义信号

```python
from flask import Flask, current_app, flash, render_template
from flask.signals import _signals

app = Flask(__name__)

# 自定义信号
xxxxx = _signals.signal('xxxxx')


def func(sender, *args, **kwargs):
    print(sender)


# 自定义信号中注册函数
xxxxx.connect(func)


@app.route("/x")
def index():
    # 触发信号
    xxxxx.send('123123', k1='v1')
    return 'Index'


if __name__ == '__main__':
    app.run()
```

3. 源码实例

- request_started

```python
class Flask(_PackageBoundObject):

    def full_dispatch_request(self):

        self.try_trigger_before_first_request_functions()
        try:
            # ############### 触发request_started 信号 ###############
            request_started.send(self)
            rv = self.preprocess_request()
            if rv is None:
                rv = self.dispatch_request()
        except Exception as e:
            rv = self.handle_user_exception(e)
        response = self.make_response(rv)
        response = self.process_response(response)

        # ############### request_finished 信号 ###############
        request_finished.send(self, response=response)
        return response

    def wsgi_app(self, environ, start_response):

        ctx = self.request_context(environ)
        ctx.push()
        error = None
        try:
            try:
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.make_response(self.handle_exception(e))
            return response(environ, start_response)
        finally:
            if self.should_ignore_error(error):
                error = None
            ctx.auto_pop(error)
```

- request_finished

```python
# 同上
```

- before_render_template

```python
def render_template(template_name_or_list, **context):
    """Renders a template from the template folder with the given
    context.

    :param template_name_or_list: the name of the template to be
                                  rendered, or an iterable with template names
                                  the first one existing will be rendered
    :param context: the variables that should be available in the
                    context of the template.
    """
    ctx = _app_ctx_stack.top
    ctx.app.update_template_context(context)
    return _render(ctx.app.jinja_env.get_or_select_template(template_name_or_list),
                   context, ctx.app)


def _render(template, context, app):
    """Renders the template and fires the signal"""

    # ############### before_render_template 信号 ###############
    before_render_template.send(app, template=template, context=context)
    rv = template.render(context)

    # ############### template_rendered 信号 ###############
    template_rendered.send(app, template=template, context=context)
    return rv
```

- template_rendered

```python
# 同上
```

- got_request_exception

```python
class Flask(_PackageBoundObject):

    def handle_exception(self, e):

        exc_type, exc_value, tb = sys.exc_info()

        # ############### got_request_exception 信号 ###############
        got_request_exception.send(self, exception=e)
        handler = self._find_error_handler(InternalServerError())

        if self.propagate_exceptions:
            # if we want to repropagate the exception, we can attempt to
            # raise it with the whole traceback in case we can do that
            # (the function was actually called from the except part)
            # otherwise, we just raise the error again
            if exc_value is e:
                reraise(exc_type, exc_value, tb)
            else:
                raise e

        self.log_exception((exc_type, exc_value, tb))
        if handler is None:
            return InternalServerError()
        return handler(e)

    def wsgi_app(self, environ, start_response):

        ctx = self.request_context(environ)
        ctx.push()
        error = None
        try:
            try:
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                # 这里这里这里这里这里这里这里这里这里这里这里这里 #
                response = self.make_response(self.handle_exception(e))
            return response(environ, start_response)
        finally:
            if self.should_ignore_error(error):
                error = None
            ctx.auto_pop(error)
```

- request_tearing_down

```python
class AppContext(object):
    def push(self):
        """Binds the app context to the current context."""
        self._refcnt += 1
        if hasattr(sys, 'exc_clear'):
            sys.exc_clear()
        _app_ctx_stack.push(self)
        # ############## 触发 appcontext_pushed 信号 ##############
        appcontext_pushed.send(self.app)

    def pop(self, exc=_sentinel):
        """Pops the app context."""
        try:
            self._refcnt -= 1
            if self._refcnt <= 0:
                if exc is _sentinel:
                    exc = sys.exc_info()[1]
                # ############## 触发 appcontext_tearing_down 信号 ##############
                self.app.do_teardown_appcontext(exc)
        finally:
            rv = _app_ctx_stack.pop()
        assert rv is self, 'Popped wrong app context.  (%r instead of %r)'
        % (rv, self)

    # ############## 触发 appcontext_popped 信号 ##############
    appcontext_popped.send(self.app)


class RequestContext(object):
    def push(self):
        top = _request_ctx_stack.top
        if top is not None and top.preserved:
            top.pop(top._preserved_exc)

        app_ctx = _app_ctx_stack.top
        if app_ctx is None or app_ctx.app != self.app:

            # ####################################################
            app_ctx = self.app.app_context()
            app_ctx.push()
            self._implicit_app_ctx_stack.append(app_ctx)
        else:
            self._implicit_app_ctx_stack.append(None)

        if hasattr(sys, 'exc_clear'):
            sys.exc_clear()

        _request_ctx_stack.push(self)

        # Open the session at the moment that the request context is
        # available. This allows a custom open_session method to use the
        # request context (e.g. code that access database information
        # stored on `g` instead of the appcontext).
        self.session = self.app.open_session(self.request)
        if self.session is None:
            self.session = self.app.make_null_session()


class Flask(_PackageBoundObject):

    def wsgi_app(self, environ, start_response):

        ctx = self.request_context(environ)
        ctx.push()
        error = None
        try:
            try:
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.make_response(self.handle_exception(e))
            return response(environ, start_response)
        finally:
            if self.should_ignore_error(error):
                error = None
            ctx.auto_pop(error)

    def pop(self, exc=_sentinel):
        app_ctx = self._implicit_app_ctx_stack.pop()

        try:
            clear_request = False
            if not self._implicit_app_ctx_stack:
                self.preserved = False
                self._preserved_exc = None
                if exc is _sentinel:
                    exc = sys.exc_info()[1]

                # ################## 触发 request_tearing_down 信号 ##################
                self.app.do_teardown_request(exc)

                # If this interpreter supports clearing the exception information
                # we do that now.  This will only go into effect on Python 2.x,
                # on 3.x it disappears automatically at the end of the exception
                # stack.
                if hasattr(sys, 'exc_clear'):
                    sys.exc_clear()

                request_close = getattr(self.request, 'close', None)
                if request_close is not None:
                    request_close()
                clear_request = True
        finally:
            rv = _request_ctx_stack.pop()

            # get rid of circular dependencies at the end of the request
            # so that we don't require the GC to be active.
            if clear_request:
                rv.request.environ['werkzeug.request'] = None

            # Get rid of the app as well if necessary.
            if app_ctx is not None:
                # ####################################################
                app_ctx.pop(exc)

            assert rv is self, 'Popped wrong request context.  '
            '(%r instead of %r)' % (rv, self)


def auto_pop(self, exc):
    if self.request.environ.get('flask._preserve_context') or
        (exc is not None and self.app.preserve_context_on_exception):
    self.preserved = True
    self._preserved_exc = exc

else:
self.pop(exc)
```

- appcontext_tearing_down

```python
# 同上
```

- appcontext_tearing_down

```python
# 同上
```

- appcontext_pushed

```python
# 同上
```

- appcontext_popped

```python
# 同上
```

- message_flashed

```python
def flash(message, category='message'):
    """Flashes a message to the next request.  In order to remove the
    flashed message from the session and to display it to the user,
    the template has to call :func:`get_flashed_messages`.

    .. versionchanged:: 0.3
       `category` parameter added.

    :param message: the message to be flashed.
    :param category: the category for the message.  The following values
                     are recommended: ``'message'`` for any kind of message,
                     ``'error'`` for errors, ``'info'`` for information
                     messages and ``'warning'`` for warnings.  However any
                     kind of string can be used as category.
    """
    # Original implementation:
    #
    #     session.setdefault('_flashes', []).append((category, message))
    #
    # This assumed that changes made to mutable structures in the session are
    # are always in sync with the session object, which is not true for session
    # implementations that use external storage for keeping their keys/values.
    flashes = session.get('_flashes', [])
    flashes.append((category, message))
    session['_flashes'] = flashes

    # ############### 触发 message_flashed 信号 ###############
    message_flashed.send(current_app._get_current_object(),
                         message=message, category=category)
```

### 五、离线脚本

1. 单app离线脚本

```python
from flask import Flask

app = Flask(__name__)

with app.app_context():
    """
    此时项目所有内容已经加载，需要所做操作处可以直接写在这里
    """
    pass
```

2. 多app离线脚本

```python
from flask import Flask

app01 = Flask("app01")
app02 = Flask("app02")

with app01.app_context():
    """
    此时app01所有内容已经加载，需要所做操作处可以直接写在这里
    """
    with app02.app_context():
        """
        此时app01所有内容已经加载，需要所做操作处可以直接写在这里        
        """
        pass
    pass
```

### 六、常用扩展组件

1. flask_session组件

```python
# session的扩展存储
# pip3 install redis
# pip3 install flask-session


from flask import Flask
from flask_session import Session
from redis import Redis

app = Flask(__name__)
app.debug = True
app.secret_key = 'djrtsfgtjhsehs'

# 配置session存储到redis中
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = Redis(host='192.168.199.103', port='6379')
Session(app)
```

2. flask_script组件

```python
from flask import Flask
from flask_script import Manager

app = Flask(__name__)

manage = Manager(app)

if __name__ == '__main__':
    manage.run()

# 如此就可以实现python manage runserver启动项目
```

3. flask-sqlalchemy

```python
# __init__.py 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# db包含了SQLAlchemy的所有操作
db = SQLAlchemy()

app = Flask(__name__)
app.config['xxxx'] = 'xxxxx'  # 写配置文件
db.init_app(app)  # 将app的所有配置文件加载，在使用SQLAlchemy时变的更加简单

if __name__ == '__main__':
    app.run()

# models.py
from sqlalchemy import Column, Integer, String
from 项目名 import db


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, unique=True)


# views.py
from 项目名 import db

# 数据库操作
db.session.query()
```

4. flask-migrate

```python
# 依赖
# flask-script
# flask-sqlalchemy
from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:00090009@192.168.199.103:3306/testmigrate?charset=utf8"
db = SQLAlchemy(app)

manager = Manager(app)
Migrate(app, db)

manager.add_command('db', MigrateCommand)


class User(db.Model):
    __tablename__ = "scriptUser"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    age = db.Column(db.Integer, default=12)


if __name__ == '__main__':
    manager.run()

"""
python manage.py db init
python manage.py db migrate # makemigrations
python manage.py db upgrade # migrate
"""
```