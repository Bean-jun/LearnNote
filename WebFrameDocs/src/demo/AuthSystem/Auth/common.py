"""
1. 数据响应 response(code:Int, msg:Str, data:Any)
2. 授权 auth_encode(**kwargs)
3. 鉴权 auth_decode(token:Str)
"""
import datetime
from http import HTTPStatus

import jwt
from django.conf import settings


def response(code=200, msg=None, data=None):
    # 请求响应
    msg = msg if msg else ""
    data = data if data else ""

    return {
        "code": code,
        "message": msg,
        "data": data
    }


def auth_encode(**kwargs):
    if not "exp" in kwargs:
        exp = settings.TOKEN_EXP
        kwargs["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=exp)
    encode = jwt.encode(kwargs, settings.SECRET_KEY, algorithm="HS256")
    return encode


def auth_decode(token):
    try:
        dicts = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256",
                           options={'verify_exp': True})
    except jwt.exceptions.ExpiredSignatureError:
        return False, response(HTTPStatus.BAD_REQUEST, "认证已过期")
    except jwt.exceptions.InvalidSignatureError:
        return False, response(HTTPStatus.BAD_REQUEST, "签名异常")
    except:
        return False, response(HTTPStatus.BAD_REQUEST, "请重新登录获取token")
    else:
        return True, response(HTTPStatus.BAD_REQUEST, "登录成功", dicts)
