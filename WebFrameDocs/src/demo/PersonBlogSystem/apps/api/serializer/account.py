from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.blog import models as blog_models
from utils.encrypt import md5


class RegisterSerializer(serializers.ModelSerializer):
    """注册账户序列化器"""
    confirm_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = blog_models.UserInfo
        fields = ['password', "confirm_password", 'username', 'email']

    def validate(self, attrs):
        # 1 确认密码是否一致
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError("请确认两次密码一致")

        # 2 确认账户是否注册过
        user = blog_models.UserInfo.objects.filter(email=attrs['email']).first()
        if user:
            raise ValidationError("该账户已经注册")

        # 3 加密密码
        attrs['password'] = md5(attrs['password'])

        # 4 确认管理员账号
        if attrs['email'] in settings.ADMIN_ACCOUNT:
            attrs['is_super'] = True

        return attrs


class LoginSerializer(serializers.ModelSerializer):
    """登录账户序列化器"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = blog_models.UserInfo
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = md5(attrs.get('password'))

        user = blog_models.UserInfo.objects.filter(email=email, password=password).first()

        if not user:
            raise ValidationError("账户或密码错误")

        attrs['user'] = user

        return attrs
