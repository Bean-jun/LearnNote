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
