from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from apps.api.serializer.account import RegisterSerializer, LoginSerializer


class RegisterAPIView(APIView):
    """用户注册"""

    # {"username": "asdfasdf", "password": "123456", "email": "xxxxx@163.com", "confirm_password": "123456"}
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data.pop('confirm_password')
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class LoginAPIView(APIView):
    """用户登录"""

    # {"email": "xxxxx@163.com", "password": "123456"}
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # 验证成功，创建用户token
            user = serializer.validated_data['user']

            # 1、根据用户生成payload
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            payload = jwt_payload_handler(user)

            # 2、加密
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            token = jwt_encode_handler(payload)

            return Response({'token': token})
        else:
            return Response({'msg': '账户或密码错误'})
