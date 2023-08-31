### 一、wsgi引入

`wsgi`通用web网关协议接口，是作为Python Web开发必须可少的标准接口，定义格式为:

```python
def app(environ, start_response):
    start_response(status, headers)
    return body
```
1. [官方引入标准库](https://docs.python.org/zh-cn/3/library/wsgiref.html)

2. 一个简单的Python web server

```python
from wsgiref.simple_server import make_server


def app(environ, start_response):
    # print("current environ: ", environ)
    headers = [("Content-type", "text/plain; charset=utf-8")]
    start_response("200 OK", headers)
    return [b"hello world"]


with make_server("0.0.0.0", 8888, app) as server:
    server.serve_forever()
```

![](image/2023-08-31-23-40-17.png)

### 二、了解Werkzeug

Werkzeug作为一个全面的wsgi工具库，为flask框架的开发提供了极大的便利。在学习flask框架之前我们对此库做一些简单的了解，将对咱们理解flask来说将会事半功倍。

1. 下载Werkzeug源码

    ```shell
    git clone https://github.com/pallets/werkzeug.git
    ```

2. 查看此项目的0.1版本(后续的说明均是基于0.1版本)

    ```shell
    git checkout 0.1
    ```

3. 目录树

   ```shell
   .
   ├── contrib      # session、限流器等
   │   ├── __init__.py
   │   ├── iterio.py
   │   ├── jsrouting.py
   │   ├── kickstart.py
   │   ├── limiter.py
   │   └── sessions.py
   ├── debug
   │   ├── __init__.py
   │   ├── render.py
   │   ├── shared
   │   └── util.py
   ├── exceptions.py # 异常
   ├── http.py      # 常用HTTP工具
   ├── __init__.py
   ├── local.py     # 本地线程 类似threading.local
   ├── routing.py   # 路由
   ├── script.py
   ├── serving.py   # HTTP Server
   ├── templates.py # 模板
   ├── testapp.py
   ├── test.py
   ├── utils.py     # 常用HTTP工具
   └── wrappers.py  # 对Request、Response进行封装
   
   3 directories, 21 files
   ```

4. 主要代码解析

- local.py
  - 参见我之前写的[Flask源码解析第一弹](https://github.com/Bean-jun/LearnNote/blob/main/WebFrameDocs/Flask-%E6%BA%90%E7%A0%81%E5%88%86%E6%9E%90.md)
- routing.py
- serving.py
- wrappers.py
  - BaseRequest    # 解析请求
    - args
    - form
    - data
    - ...
  - BaseResponse   # 请求响应
    - write
    - set_cookie
    - ...

### 三、尝试自定义短链接应用(Werkzeug官方Demo)

1. [教程地址](https://werkzeug.palletsprojects.com/en/2.2.x/tutorial/)

2. 源码解析

    ```python
    """A simple URL shortener using Werkzeug and redis."""
    import os
    from urllib.parse import urlsplit

    import redis
    from jinja2 import Environment
    from jinja2 import FileSystemLoader
    from werkzeug.exceptions import HTTPException
    from werkzeug.exceptions import NotFound
    from werkzeug.middleware.shared_data import SharedDataMiddleware
    from werkzeug.routing import Map
    from werkzeug.routing import Rule
    from werkzeug.utils import redirect
    from werkzeug.wrappers import Request
    from werkzeug.wrappers import Response


    def base36_encode(number):
        assert number >= 0, "positive integer required"
        if number == 0:
            return "0"
        base36 = []
        while number != 0:
            number, i = divmod(number, 36)
            base36.append("0123456789abcdefghijklmnopqrstuvwxyz"[i])
        return "".join(reversed(base36))


    def is_valid_url(url):
        parts = urlsplit(url)
        return parts.scheme in ("http", "https")


    def get_hostname(url):
        return urlsplit(url).netloc


    class Shortly:
        def __init__(self, config):
            # APP初始化，使用Redis对短链接进行存储
            self.redis = redis.Redis(
                config["redis_host"], config["redis_port"], decode_responses=True
            )
            # 添加jinja模板
            template_path = os.path.join(os.path.dirname(__file__), "templates")
            self.jinja_env = Environment(
                loader=FileSystemLoader(template_path), autoescape=True
            )
            self.jinja_env.filters["hostname"] = get_hostname

            # 配置Url请求
            self.url_map = Map(
                [
                    Rule("/", endpoint="new_url"),
                    Rule("/<short_id>", endpoint="follow_short_link"),
                    Rule("/<short_id>+", endpoint="short_link_details"),
                ]
            )

        def on_new_url(self, request):
            error = None
            url = ""
            if request.method == "POST":
                url = request.form["url"]
                if not is_valid_url(url):
                    error = "Please enter a valid URL"
                else:
                    short_id = self.insert_url(url)
                    return redirect(f"/{short_id}+")
            return self.render_template("new_url.html", error=error, url=url)

        def on_follow_short_link(self, request, short_id):
            link_target = self.redis.get(f"url-target:{short_id}")
            if link_target is None:
                raise NotFound()
            self.redis.incr(f"click-count:{short_id}")
            return redirect(link_target)

        def on_short_link_details(self, request, short_id):
            link_target = self.redis.get(f"url-target:{short_id}")
            if link_target is None:
                raise NotFound()
            click_count = int(self.redis.get(f"click-count:{short_id}") or 0)
            return self.render_template(
                "short_link_details.html",
                link_target=link_target,
                short_id=short_id,
                click_count=click_count,
            )

        def error_404(self):
            response = self.render_template("404.html")
            response.status_code = 404
            return response

        def insert_url(self, url):
            short_id = self.redis.get(f"reverse-url:{url}")
            if short_id is not None:
                return short_id
            url_num = self.redis.incr("last-url-id")
            short_id = base36_encode(url_num)
            self.redis.set(f"url-target:{short_id}", url)
            self.redis.set(f"reverse-url:{url}", short_id)
            return short_id

        def render_template(self, template_name, **context):
            t = self.jinja_env.get_template(template_name)
            return Response(t.render(context), mimetype="text/html")

        def dispatch_request(self, request):
            adapter = self.url_map.bind_to_environ(request.environ)
            try:
                # 匹配功能函数进行调用
                endpoint, values = adapter.match()
                # 反射函数并执行，由于没有使用local对象，使得对应视图函数类似Django的写法，需要传递Request对象
                return getattr(self, f"on_{endpoint}")(request, **values)
            except NotFound:
                return self.error_404()
            except HTTPException as e:
                return e

        def wsgi_app(self, environ, start_response):
            # 封装Request
            request = Request(environ)
            # 对请求进行分发
            response = self.dispatch_request(request)
            # 封装response并响应
            return response(environ, start_response)

        # run_simple执行流程到达execute时，会调用当前对象__call__方法
        def __call__(self, environ, start_response):
            return self.wsgi_app(environ, start_response)


    def create_app(redis_host="localhost", redis_port=6379, with_static=True):
        # 创建一个Shortly应用
        app = Shortly({"redis_host": redis_host, "redis_port": redis_port})
        if with_static:
            app.wsgi_app = SharedDataMiddleware(
                app.wsgi_app, {"/static": os.path.join(os.path.dirname(__file__), "static")}
            )
        return app


    if __name__ == "__main__":
        from werkzeug.serving import run_simple

        app = create_app()
        # 将应用丢入run_simple中执行
        run_simple("127.0.0.1", 5000, app, use_debugger=True, use_reloader=True)

        # run_simple执行流程
        # run_simple --> make_server 
        # --> BaseWSGIServer(绑定handler(WSGIRequestHandler)) 
        # --> BaseWSGIServer.serve_forever
        # --> HTTPServer.serve_forever --> _handle_request_noblock 
        # --> process_request --> finish_request
        # --> RequestHandlerClass(request, client_address, self)(绑定server到handler上[self])
        # --> WSGIRequestHandler.handle
        # --> BaseHTTPRequestHandler.handle
        # --> WSGIRequestHandler.handle_one_request
        # --> WSGIRequestHandler.run_wsgi()
        # --> WSGIRequestHandler.execute(self.server.app)
        # --> execute执行 内部[application_iter = app(environ, start_response)]
    ```

### 四、Flask官方demo

1. 下载flask源码

    ```shell
    git clone https://github.com/pallets/flask.git
    ```

2. 查看此项目的0.1版本(后续的说明均是基于0.1版本)

    ```shell
    git checkout 0.1
    ```

3. 目录树

    ```shell
    .
    ├── artwork
    ├── docs
    ├── examples
    │   ├── flaskr
    │   └── minitwit
    ├── flask.py
    ├── LICENSE
    ├── Makefile
    ├── README
    ├── setup.py
    ├── tests
    │   ├── flask_tests.py
    │   ├── static
    │   └── templates
    └── website
        ├── index.html
        └── logo.png
    ```

4. 0.1 源码(部分)

```python

class Flask(object):
    """The flask object implements a WSGI application and acts as the central
    object.  It is passed the name of the module or package of the
    application.  Once it is created it will act as a central registry for
    the view functions, the URL rules, template configuration and much more.

    The name of the package is used to resolve resources from inside the
    package or the folder the module is contained in depending on if the
    package parameter resolves to an actual python package (a folder with
    an `__init__.py` file inside) or a standard module (just a `.py` file).

    For more information about resource loading, see :func:`open_resource`.

    Usually you create a :class:`Flask` instance in your main module or
    in the `__init__.py` file of your package like this::

        from flask import Flask
        app = Flask(__name__)
    """

    #: the class that is used for request objects.  See :class:`~flask.request`
    #: for more information.
    request_class = Request

    #: the class that is used for response objects.  See
    #: :class:`~flask.Response` for more information.
    response_class = Response

    #: path for the static files.  If you don't want to use static files
    #: you can set this value to `None` in which case no URL rule is added
    #: and the development server will no longer serve any static files.
    static_path = '/static'

    #: if a secret key is set, cryptographic components can use this to
    #: sign cookies and other things.  Set this to a complex random value
    #: when you want to use the secure cookie for instance.
    secret_key = None

    #: The secure cookie uses this for the name of the session cookie
    session_cookie_name = 'session'

    #: options that are passed directly to the Jinja2 environment
    jinja_options = dict(
        autoescape=True,
        extensions=['jinja2.ext.autoescape', 'jinja2.ext.with_']
    )

    def __init__(self, package_name):
        #: the debug flag.  Set this to `True` to enable debugging of
        #: the application.  In debug mode the debugger will kick in
        #: when an unhandled exception ocurrs and the integrated server
        #: will automatically reload the application if changes in the
        #: code are detected.
        self.debug = False

        #: the name of the package or module.  Do not change this once
        #: it was set by the constructor.
        self.package_name = package_name

        #: where is the app root located?
        self.root_path = _get_package_path(self.package_name)

        #: a dictionary of all view functions registered.  The keys will
        #: be function names which are also used to generate URLs and
        #: the values are the function objects themselves.
        #: to register a view function, use the :meth:`route` decorator.
        self.view_functions = {}

        #: a dictionary of all registered error handlers.  The key is
        #: be the error code as integer, the value the function that
        #: should handle that error.
        #: To register a error handler, use the :meth:`errorhandler`
        #: decorator.
        self.error_handlers = {}

        #: a list of functions that should be called at the beginning
        #: of the request before request dispatching kicks in.  This
        #: can for example be used to open database connections or
        #: getting hold of the currently logged in user.
        #: To register a function here, use the :meth:`before_request`
        #: decorator.
        self.before_request_funcs = []

        #: a list of functions that are called at the end of the
        #: request.  Tha function is passed the current response
        #: object and modify it in place or replace it.
        #: To register a function here use the :meth:`after_request`
        #: decorator.
        self.after_request_funcs = []

        #: a list of functions that are called without arguments
        #: to populate the template context.  Each returns a dictionary
        #: that the template context is updated with.
        #: To register a function here, use the :meth:`context_processor`
        #: decorator.
        self.template_context_processors = [_default_template_ctx_processor]

        self.url_map = Map()

        if self.static_path is not None:
            self.url_map.add(Rule(self.static_path + '/<filename>',
                                  build_only=True, endpoint='static'))
            if pkg_resources is not None:
                target = (self.package_name, 'static')
            else:
                target = os.path.join(self.root_path, 'static')
            self.wsgi_app = SharedDataMiddleware(self.wsgi_app, {
                self.static_path: target
            })

        #: the Jinja2 environment.  It is created from the
        #: :attr:`jinja_options` and the loader that is returned
        #: by the :meth:`create_jinja_loader` function.
        self.jinja_env = Environment(loader=self.create_jinja_loader(),
                                     **self.jinja_options)
        self.jinja_env.globals.update(
            url_for=url_for,
            get_flashed_messages=get_flashed_messages
        )

    def create_jinja_loader(self):
        """Creates the Jinja loader.  By default just a package loader for
        the configured package is returned that looks up templates in the
        `templates` folder.  To add other loaders it's possible to
        override this method.
        """
        if pkg_resources is None:
            return FileSystemLoader(os.path.join(self.root_path, 'templates'))
        return PackageLoader(self.package_name)

    def update_template_context(self, context):
        """Update the template context with some commonly used variables.
        This injects request, session and g into the template context.

        :param context: the context as a dictionary that is updated in place
                        to add extra variables.
        """
        reqctx = _request_ctx_stack.top
        for func in self.template_context_processors:
            context.update(func())

    def run(self, host='localhost', port=5000, **options):
        """Runs the application on a local development server.  If the
        :attr:`debug` flag is set the server will automatically reload
        for code changes and show a debugger in case an exception happened.

        :param host: the hostname to listen on.  set this to ``'0.0.0.0'``
                     to have the server available externally as well.
        :param port: the port of the webserver
        :param options: the options to be forwarded to the underlying
                        Werkzeug server.  See :func:`werkzeug.run_simple`
                        for more information.
        """
        from werkzeug import run_simple
        if 'debug' in options:
            self.debug = options.pop('debug')
        options.setdefault('use_reloader', self.debug)
        options.setdefault('use_debugger', self.debug)
        return run_simple(host, port, self, **options)

    def test_client(self):
        """Creates a test client for this application.  For information
        about unit testing head over to :ref:`testing`.
        """
        from werkzeug import Client
        return Client(self, self.response_class, use_cookies=True)

    def open_resource(self, resource):
        """Opens a resource from the application's resource folder.  To see
        how this works, consider the following folder structure::

            /myapplication.py
            /schemal.sql
            /static
                /style.css
            /template
                /layout.html
                /index.html

        If you want to open the `schema.sql` file you would do the
        following::

            with app.open_resource('schema.sql') as f:
                contents = f.read()
                do_something_with(contents)

        :param resource: the name of the resource.  To access resources within
                         subfolders use forward slashes as separator.
        """
        if pkg_resources is None:
            return open(os.path.join(self.root_path, resource), 'rb')
        return pkg_resources.resource_stream(self.package_name, resource)

    def open_session(self, request):
        """Creates or opens a new session.  Default implementation stores all
        session data in a signed cookie.  This requires that the
        :attr:`secret_key` is set.

        :param request: an instance of :attr:`request_class`.
        """
        key = self.secret_key
        if key is not None:
            return SecureCookie.load_cookie(request, self.session_cookie_name,
                                            secret_key=key)

    def save_session(self, session, response):
        """Saves the session if it needs updates.  For the default
        implementation, check :meth:`open_session`.

        :param session: the session to be saved (a
                        :class:`~werkzeug.contrib.securecookie.SecureCookie`
                        object)
        :param response: an instance of :attr:`response_class`
        """
        if session is not None:
            session.save_cookie(response, self.session_cookie_name)

    def add_url_rule(self, rule, endpoint, **options):
        """Connects a URL rule.  Works exactly like the :meth:`route`
        decorator but does not register the view function for the endpoint.

        Basically this example::

            @app.route('/')
            def index():
                pass

        Is equivalent to the following::

            def index():
                pass
            app.add_url_rule('index', '/')
            app.view_functions['index'] = index

        :param rule: the URL rule as string
        :param endpoint: the endpoint for the registered URL rule.  Flask
                         itself assumes the name of the view function as
                         endpoint
        :param options: the options to be forwarded to the underlying
                        :class:`~werkzeug.routing.Rule` object
        """
        options['endpoint'] = endpoint
        options.setdefault('methods', ('GET',))
        self.url_map.add(Rule(rule, **options))

    def route(self, rule, **options):
        """A decorator that is used to register a view function for a
        given URL rule.  Example::

            @app.route('/')
            def index():
                return 'Hello World'

        Variables parts in the route can be specified with angular
        brackets (``/user/<username>``).  By default a variable part
        in the URL accepts any string without a slash however a different
        converter can be specified as well by using ``<converter:name>``.

        Variable parts are passed to the view function as keyword
        arguments.

        The following converters are possible:

        =========== ===========================================
        `int`       accepts integers
        `float`     like `int` but for floating point values
        `path`      like the default but also accepts slashes
        =========== ===========================================

        Here some examples::

            @app.route('/')
            def index():
                pass

            @app.route('/<username>')
            def show_user(username):
                pass

            @app.route('/post/<int:post_id>')
            def show_post(post_id):
                pass

        An important detail to keep in mind is how Flask deals with trailing
        slashes.  The idea is to keep each URL unique so the following rules
        apply:

        1. If a rule ends with a slash and is requested without a slash
           by the user, the user is automatically redirected to the same
           page with a trailing slash attached.
        2. If a rule does not end with a trailing slash and the user request
           the page with a trailing slash, a 404 not found is raised.

        This is consistent with how web servers deal with static files.  This
        also makes it possible to use relative link targets safely.

        The :meth:`route` decorator accepts a couple of other arguments
        as well:

        :param rule: the URL rule as string
        :param methods: a list of methods this rule should be limited
                        to (``GET``, ``POST`` etc.).  By default a rule
                        just listens for ``GET`` (and implicitly ``HEAD``).
        :param subdomain: specifies the rule for the subdoain in case
                          subdomain matching is in use.
        :param strict_slashes: can be used to disable the strict slashes
                               setting for this rule.  See above.
        :param options: other options to be forwarded to the underlying
                        :class:`~werkzeug.routing.Rule` object.
        """
        def decorator(f):
            self.add_url_rule(rule, f.__name__, **options)
            self.view_functions[f.__name__] = f
            return f
        return decorator

    def errorhandler(self, code):
        """A decorator that is used to register a function give a given
        error code.  Example::

            @app.errorhandler(404)
            def page_not_found():
                return 'This page does not exist', 404

        You can also register a function as error handler without using
        the :meth:`errorhandler` decorator.  The following example is
        equivalent to the one above::

            def page_not_found():
                return 'This page does not exist', 404
            app.error_handlers[404] = page_not_found

        :param code: the code as integer for the handler
        """
        def decorator(f):
            self.error_handlers[code] = f
            return f
        return decorator

    def before_request(self, f):
        """Registers a function to run before each request."""
        self.before_request_funcs.append(f)
        return f

    def after_request(self, f):
        """Register a function to be run after each request."""
        self.after_request_funcs.append(f)
        return f

    def context_processor(self, f):
        """Registers a template context processor function."""
        self.template_context_processors.append(f)
        return f

    def match_request(self):
        """Matches the current request against the URL map and also
        stores the endpoint and view arguments on the request object
        is successful, otherwise the exception is stored.
        """
        rv = _request_ctx_stack.top.url_adapter.match()
        request.endpoint, request.view_args = rv
        return rv

    def dispatch_request(self):
        """Does the request dispatching.  Matches the URL and returns the
        return value of the view or error handler.  This does not have to
        be a response object.  In order to convert the return value to a
        proper response object, call :func:`make_response`.
        """
        try:
            endpoint, values = self.match_request()
            return self.view_functions[endpoint](**values)
        except HTTPException, e:
            handler = self.error_handlers.get(e.code)
            if handler is None:
                return e
            return handler(e)
        except Exception, e:
            handler = self.error_handlers.get(500)
            if self.debug or handler is None:
                raise
            return handler(e)

    def make_response(self, rv):
        """Converts the return value from a view function to a real
        response object that is an instance of :attr:`response_class`.

        The following types are allowd for `rv`:

        ======================= ===========================================
        :attr:`response_class`  the object is returned unchanged
        :class:`str`            a response object is created with the
                                string as body
        :class:`unicode`        a response object is created with the
                                string encoded to utf-8 as body
        :class:`tuple`          the response object is created with the
                                contents of the tuple as arguments
        a WSGI function         the function is called as WSGI application
                                and buffered as response object
        ======================= ===========================================

        :param rv: the return value from the view function
        """
        if isinstance(rv, self.response_class):
            return rv
        if isinstance(rv, basestring):
            return self.response_class(rv)
        if isinstance(rv, tuple):
            return self.response_class(*rv)
        return self.response_class.force_type(rv, request.environ)

    def preprocess_request(self):
        """Called before the actual request dispatching and will
        call every as :meth:`before_request` decorated function.
        If any of these function returns a value it's handled as
        if it was the return value from the view and further
        request handling is stopped.
        """
        for func in self.before_request_funcs:
            rv = func()
            if rv is not None:
                return rv

    def process_response(self, response):
        """Can be overridden in order to modify the response object
        before it's sent to the WSGI server.  By default this will
        call all the :meth:`after_request` decorated functions.

        :param response: a :attr:`response_class` object.
        :return: a new response object or the same, has to be an
                 instance of :attr:`response_class`.
        """
        session = _request_ctx_stack.top.session
        if session is not None:
            self.save_session(session, response)
        for handler in self.after_request_funcs:
            response = handler(response)
        return response

    def wsgi_app(self, environ, start_response):
        """The actual WSGI application.  This is not implemented in
        `__call__` so that middlewares can be applied:

            app.wsgi_app = MyMiddleware(app.wsgi_app)

        :param environ: a WSGI environment
        :param start_response: a callable accepting a status code,
                               a list of headers and an optional
                               exception context to start the response
        """
        with self.request_context(environ):
            rv = self.preprocess_request()
            if rv is None:
                rv = self.dispatch_request()
            response = self.make_response(rv)
            response = self.process_response(response)
            return response(environ, start_response)

    def request_context(self, environ):
        """Creates a request context from the given environment and binds
        it to the current context.  This must be used in combination with
        the `with` statement because the request is only bound to the
        current context for the duration of the `with` block.

        Example usage::

            with app.request_context(environ):
                do_something_with(request)

        :params environ: a WSGI environment
        """
        return _RequestContext(self, environ)

    def test_request_context(self, *args, **kwargs):
        """Creates a WSGI environment from the given values (see
        :func:`werkzeug.create_environ` for more information, this
        function accepts the same arguments).
        """
        return self.request_context(create_environ(*args, **kwargs))

    def __call__(self, environ, start_response):
        """Shortcut for :attr:`wsgi_app`"""
        return self.wsgi_app(environ, start_response)

```

