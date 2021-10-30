import json
from functools import wraps
from http import HTTPStatus

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django_redis import get_redis_connection

from Auth.models import User

from Auth.common import response, auth_decode

redis_client = get_redis_connection()


class UserSecret():

    def __init__(self, secret_id, redirect_uri):
        self.secret_id = secret_id
        self.redirect_uri = redirect_uri


@method_decorator(csrf_exempt, "dispatch")
class BaseView(View):
    """
    用于处理类之外的请求方式修正
    """

    @staticmethod
    def exception_func(request, *args, **kwargs):
        return JsonResponse(response(code=HTTPStatus.METHOD_NOT_ALLOWED, msg=f"{request.method}请求方式被禁止"))

    @staticmethod
    def parse_request_body(request, *args, **kwargs):
        try:
            dict = json.loads(request.body.decode())
        except Exception as e:
            try:
                dict = request.POST
            except Exception as e:
                raise e
            else:
                for k, v in dict.items():
                    kwargs[k] = v
        else:
            for k, v in dict.items():
                kwargs[k] = v

        return kwargs

    def parse_params_developer(self):
        # 解析请求secret_id, redirect_uri
        secret_id = self.request.GET.get("secret_id")
        redirect_uri = self.request.GET.get("redirect_uri")

        if not all([secret_id, redirect_uri]):
            return JsonResponse(response(HTTPStatus.NOT_ACCEPTABLE, "请确认请求URL是否异常"))

        self.request.user_secret = UserSecret(secret_id, redirect_uri)

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), None)
        else:
            handler = None

        # 解析前端请求
        kwargs = BaseView.parse_request_body(request, *args, **kwargs)

        if handler:
            return handler(request, *args, **kwargs)
        else:
            return BaseView.exception_func(request, *args, **kwargs)


class BaseAuthView(BaseView):
    """
    jwt权限认证类
    """

    @staticmethod
    def auth(f):
        @wraps(f)
        def inner(self, request, *args, **kwargs):
            Authorization = request.headers.get("Authorization")
            if not Authorization:
                return JsonResponse(response(HTTPStatus.FORBIDDEN, "请设置Authorization"))

            flag, msg = auth_decode(Authorization)
            if not flag:
                return JsonResponse(msg)
            try:
                email = msg.get("data").get("email")
            except Exception as e:
                return JsonResponse(response(HTTPStatus.INTERNAL_SERVER_ERROR, "服务器内部异常"))

            user = User.objects.filter(email=email).first()
            kwargs["inner_user"] = user

            return f(self, request, *args, **kwargs)

        return inner
