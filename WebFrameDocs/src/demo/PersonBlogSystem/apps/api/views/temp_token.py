from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.auth.auth import LoginParamAuthentication
from utils.encrypt import add_salt


class GetToken(APIView):
    """获取语雀token"""
    authentication_classes = [LoginParamAuthentication, ]

    def get(self, request, *args, **kwargs):
        if request.user.email in settings.ADMIN_ACCOUNT:
            return Response({"msg": add_salt(settings.YUQUE_TOKEN), "status": 200})
        else:
            return Response({"msg": "请使用管理员账号", "status": 400})
