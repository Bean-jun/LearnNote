import json
import uuid
from http import HTTPStatus

from django.conf import settings
from django.http import JsonResponse

from Auth.common import response, auth_encode
from Auth.form.account import UserRegisterForm, UserLoginForm
from ._base import BaseView, redis_client


class RegisterView(BaseView):

    @staticmethod
    def post(request, *args, **kwargs):

        form = UserRegisterForm(request=request, data=kwargs)

        if form.is_valid():

            form.instance.save()

            return JsonResponse(response(code=HTTPStatus.OK,
                                         msg="注册成功",
                                         data={
                                             "token": auth_encode(username=form.cleaned_data["username"],
                                                                  email=form.cleaned_data["email"]),
                                             "username": form.cleaned_data["username"],
                                             "email": form.cleaned_data["email"],
                                         }))
        else:
            return JsonResponse(response(code=HTTPStatus.EXPECTATION_FAILED, msg="校验数据异常", data=request.error))


class LoginView(BaseView):

    def post(self, *args, **kwargs):

        develop_oauth_flag = False

        # 处理开发者授权的用户登录
        if not self.parse_params_developer():
            develop_oauth_flag = True

        form = UserLoginForm(request=self.request, data=kwargs)

        if form.is_valid():

            user = form.cleaned_data["inner_user"]

            val = {
                "username": user.username,
                "email": user.email,
            }
            data = {
                "token": auth_encode(username=user.username,
                                     email=user.email),
                "redirect_uri": "",
                "authorization_code": ""
            }

            # 授权成功的，使用开发者网站回调的用户需要将信息写入redis, 前端需要根据redirect_uri的值跳转
            if develop_oauth_flag:
                code = str(uuid.uuid4())
                key = self.request.user_secret.secret_id + code
                data["redirect_uri"] = self.request.user_secret.redirect_uri
                data["authorization_code"] = code
                redis_client.setex(name=key, value=json.dumps(val), time=settings.OAUTH_EXP)

            data.update(val)

            return JsonResponse(response(code=HTTPStatus.OK,
                                         msg="登录成功",
                                         data=data
                                         ))

        else:
            return JsonResponse(response(code=HTTPStatus.UNAUTHORIZED, msg="登录数据异常", data=self.request.error))
