def response(code=200, msg=None, data=None):
    # 请求响应
    msg = msg if msg else ""
    data = data if data else ""

    return {
        "code": code,
        "message": msg,
        "data": data
    }
