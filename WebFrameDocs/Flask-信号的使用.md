# flask blinker 使用测试

相关源码见`./src/flask_signal.py`

## 一、注意

> 信号在接收时，完全支持 请求情境 。在 request_started 和 request_finished 本地环境变量 始终可用。因此你可以依赖 flask.g 及其他本地环境变量。 请注意在 发送信号 中所述的限制和 request_tearing_down 信号。

## 二、说明(信号在上下文)

1. 使用blinker自定义信号

    ```python
    from blinker import Namespace

    my_signals = Namespace()
    # 创建别名 用于信号的发送、订阅、取消订阅等（信号名唯一）
    xxx_save = my_signals.signal('model-saved')
    ```

2. 在合理的位置发送信号

    ```python
    # 第一个参数为：发送者，第二个参数可选 
    xxx_save.send("index",name="index")
    ```

3. 订阅信号(在信号被发送时被触发)

    ```python
    # 第一个参数是当信号发出时所调用的函数。第二个参数是可选参数，定义一个发送者
    def pprint(*args, **kwargs):
        print(app.config)
        print("_______%s________" % __name__, args, kwargs, g.user)

    xxx_save.connect(pprint)
    ```

4. 取消信号订阅

    ```python
    # 关闭订阅
    xxx_save.disconnect(pprint)
    ```
