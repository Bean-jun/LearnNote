1. 起因

    临时有一个赛事需求，需要紧急上线几组接口，用于支持赛事的进行。这里主要涉及的两个接口分别是：
    1. 获取当前实验下的所有资料信息
    2. 获取当前实验下的公告信息

2. 问题表现

    1. 接口1返回数据正常
    2. 接口2返回了其他奇怪的公告信息，或者不显示

3. 问题排查

    这个问题其实很奇怪，接口单独测试都正常，但是一放到一起就出问题了。直到看到小伙伴写的接口后，我才发现，原来是默认参数的问题。

    在说之前，我先放一段代码和这段代码的运行结果。
    ```python
    import typing as t

    from flask import Flask, request
    from flask.views import MethodView as _View

    app = Flask(__name__)


    class View(_View):

        def __init__(
            self,
            funs: t.Dict[str, t.Callable[[t.Dict[str, t.Any]], None]] = dict(),
        ):
            super().__init__()
            self.funs = funs

        def out(
            self, msg: t.Dict[str, t.Any], cook_fun: t.Callable[[t.Dict[str, t.Any]], None]
        ):
            if cook_fun:
                cook_fun(msg)
            return msg

        def get(self):
            msg = {
                "msg": "Hello from py-default-args-bug!",
                "status": "success",
                "data": {},
            }

            cook_fun = None
            if "get" in self.funs:
                cook_fun = self.funs["get"]

            return self.out(msg, cook_fun)


    class AView(View):

        def __init__(self):
            super().__init__(funs={"get": self.cook_get})

        def cook_get(self, msg: t.Dict[str, t.Any]):
            msg["_cook"] = "AView"


    class BView(View):

        def __init__(self):
            super().__init__()

        def cook_get_1(self, msg: t.Dict[str, t.Any]):
            msg["_cook"] = "BView_1"

        def cook_get_2(self, msg: t.Dict[str, t.Any]):
            msg["_cook"] = "BView_2"

        def get(self):
            if request.args.get("Q") == "1":
                self.funs["get"] = self.cook_get_1
            else:
                self.funs["get"] = self.cook_get_2
            return super().get()


    class CView(View):

        def __init__(self):
            super().__init__()

        def get(self):
            print(self.funs)
            return super().get()


    app.add_url_rule("/a", view_func=AView.as_view("a"))
    app.add_url_rule("/b", view_func=BView.as_view("b"))
    app.add_url_rule("/c", view_func=CView.as_view("c"))

    if __name__ == "__main__":
        app.run(debug=True)
    ```
    运行结果：
    ```shell
    (py-default-args-bug) C:\LearnNote\BugDocs\src\py_default_args_bug>curl http://127.0.0.1:5000/c
    {
    "data": {},
    "msg": "Hello from py-default-args-bug!",
    "status": "success"
    }

    (py-default-args-bug) C:\LearnNote\BugDocs\src\py_default_args_bug>curl http://127.0.0.1:5000/a
    {
    "_cook": "AView",
    "data": {},
    "msg": "Hello from py-default-args-bug!",
    "status": "success"
    }

    (py-default-args-bug) C:\LearnNote\BugDocs\src\py_default_args_bug>curl http://127.0.0.1:5000/b
    {
    "_cook": "BView_2",
    "data": {},
    "msg": "Hello from py-default-args-bug!",
    "status": "success"
    }

    (py-default-args-bug) C:\LearnNote\BugDocs\src\py_default_args_bug>curl http://127.0.0.1:5000/c
    {
    "_cook": "BView_2",
    "data": {},
    "msg": "Hello from py-default-args-bug!",
    "status": "success"
    }

    (py-default-args-bug) C:\LearnNote\BugDocs\src\py_default_args_bug>curl http://127.0.0.1:5000/b?Q=1
    {
    "_cook": "BView_1",
    "data": {},
    "msg": "Hello from py-default-args-bug!",
    "status": "success"
    }

    (py-default-args-bug) C:\LearnNote\BugDocs\src\py_default_args_bug>curl http://127.0.0.1:5000/c    
    {
    "_cook": "BView_1",
    "data": {},
    "msg": "Hello from py-default-args-bug!",
    "status": "success"
    }
    ```

    居然在方法中使用了可变的默认参数，导致了这个问题。到这里就有小伙伴问了，为什么之前没有这种情况。

    其实很简单，因为之前都是`AView`那种写法，没有使用可变的默认参数，所以没有出现这个问题。

    对这个不理解的小伙伴，可以参考一下`流畅的Python`一书中提及的幽灵公交案例。

4. 解决过程

    禁止在函数、方法中使用这种默认参数，直接修改源码`View`，如下

    ```python
    class View(_View):

        def __init__(
            self,
            funs: t.Optional[t.Dict[str, t.Callable[[t.Dict[str, t.Any]], None]]] = None,
        ):
            super().__init__()
            if funs is None:
                funs = dict()
            self.funs = funs
    ```