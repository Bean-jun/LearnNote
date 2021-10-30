"""
用户授权部分
获取随机字符码--
"""
import json
from http import HTTPStatus

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect

from Auth.common import response
from Auth.models import User
from ._base import BaseView, redis_client

"""
oauth 授权网站地址
http://127.0.0.1:8000/oauth?secret_id=xxx&redirect_uri=xxxx
"""


class Oauth(BaseView):

    def get(self, *args, **kwargs):
        """开发者请求，获取登录授权页面给用户"""
        if ret := self.parse_params_developer():  # 海象运算符
            return ret

        try:
            user = User.objects.get(secret_id=self.request.user_secret.secret_id)
        except User.DoesNotExist:
            return JsonResponse(response(HTTPStatus.FORBIDDEN, "授权码异常"))

        # 授权登录页面-前端授权页面地址
        authorization_index = "{}?secret_id={}&redirect_uri={}".format(settings.HTML_OAUTH, user.secret_id, self.request.user_secret.redirect_uri)
        return redirect(authorization_index)

    def post(self, *args, **kwargs):
        # 用户授权页面，授权后将信息写入redis, 这里需要开发者使用secret_id, secret_value, code进行内容的获取
        secret_id = kwargs.get("secret_id")
        secret_value = kwargs.get("secret_value")
        code = kwargs.get("authorization_code")

        if not all([secret_id, secret_value, code]):
            return JsonResponse(response(HTTPStatus.TOO_EARLY, "请确认请求体是否异常"))

        # 校验用户合法性
        try:
            user = User.objects.get(secret_id=secret_id, secret_value=secret_value)
        except User.DoesNotExist:
            return JsonResponse(response(HTTPStatus.FORBIDDEN, "开发者账号秘钥异常"))

        key = "{}{}".format(user.secret_id, code)
        val = redis_client.get(name=key)

        if not val:
            return JsonResponse(response(HTTPStatus.FORBIDDEN, "用户授权失败"))

        return JsonResponse(response(HTTPStatus.OK, msg="获取授权成功", data=json.loads(val)))
