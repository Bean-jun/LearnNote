import datetime
from functools import wraps

import jwt
from flask import request, current_app
from flask_restful import Resource

from apps.api.common.response import response
from apps.models import UserInfo


class BaseView(Resource):

    def get(self):
        return response(400, f"{request.method}请求方式异常")

    def post(self):
        return response(400, f"{request.method}请求方式异常")

    def delete(self):
        return response(400, f"{request.method}请求方式异常")

    def put(self):
        return response(400, f"{request.method}请求方式异常")

    def token_encode(self, **kwargs):
        if not "exp" in kwargs:
            exp = current_app.config.get("TOKEN_EXP")
            kwargs["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=exp)
        encode = jwt.encode(kwargs, current_app.config.get("SECRET_KEY"), algorithm="HS256")
        return encode

    @staticmethod
    def _token_decode(token):
        try:
            msg_dict = jwt.decode(token, current_app.config.get("SECRET_KEY"), algorithms="HS256",
                                  options={'verify_exp': True})
        except jwt.exceptions.ExpiredSignatureError:
            return False, response(400, "认证已过期")
        except jwt.exceptions.InvalidSignatureError:
            return False, response(400, "签名异常")
        except:
            return False, response(400, "请重新登录获取token")
        else:
            return True, response(200, "登录成功", msg_dict)

    @staticmethod
    def auth(f):

        @wraps(f)
        def inner(*args, **kwargs):
            flag, msg = BaseView._token_decode(request.headers.get("Authorization"))
            if not flag:
                return msg

            # 非管理员无法操作
            try:
                email = msg.get("data").get("email")
            except Exception as e:
                return response(400, "服务器内部异常")

            if email not in current_app.config.get("SUPER_USER"):
                return response(400, "非管理员账号请勿操作")

            user = UserInfo.query.filter_by(email=email).first()
            kwargs["user"] = user

            return f(*args, **kwargs)

        return inner
