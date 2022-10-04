"""
pip install flask
pip install blinker
"""

from flask import Flask, g
from blinker import Namespace

app = Flask(__name__)

# 创建信号
my_signals = Namespace()
xxx_save = my_signals.signal('model-saved')

@app.before_request
def before():
    g.user = "tom"

@app.route("/")
def index():
    xxx_save.send("index",name="index")
    return "hello word"

def pprint(*args, **kwargs):
    # print(app.config)
    print("_______%s________" % __name__, args, kwargs, g.user)

    # 关闭订阅
    xxx_save.disconnect(pprint)


# 订阅信号，当接收到信号时触发对应函数
xxx_save.connect(pprint)

if __name__ == "__main__":
    app.run(debug=True)
