import jwt
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.settings import api_settings

from apps.blog.models import UserInfo


class LoginParamAuthentication(BaseAuthentication):
    """用户登录认证"""

    def authenticate(self, request):
        token = request.query_params.get('token', None)

        if not token:
            raise exceptions.AuthenticationFailed({"msg": "请登录之后操作"})

        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed({"msg": "登录超时"})
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed({"msg": "格式错误"})
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed({"msg": "认证失败"})

        user = UserInfo.objects.filter(email=payload['email']).first()

        return user, token
