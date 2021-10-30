from django import forms
from django.forms import ValidationError

from apps.blog.forms.bootstrap import BootStrapForm
from apps.blog.models import UserInfo
from utils.encrypt import md5


class RegisterForm(BootStrapForm, forms.ModelForm):
    """用户注册校验"""
    email = forms.EmailField(label='邮箱地址')

    password = forms.CharField(label='密码',
                               min_length=8,
                               max_length=32,
                               error_messages={
                                   'min_length': '密码不易太短',
                                   'max_length': '密码不易太长',
                               },
                               widget=forms.PasswordInput())

    confirm_password = forms.CharField(label='重复密码',
                                       min_length=8,
                                       max_length=32,
                                       error_messages={
                                           'min_length': '密码不易太短',
                                           'max_length': '密码不易太长',
                                       },
                                       widget=forms.PasswordInput())

    class Meta:
        model = UserInfo
        fields = ['username', 'email', 'password']

    def clean_email(self):
        """校验邮箱"""
        email = self.cleaned_data['email']

        exists = UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError("该邮箱已注册")

        return email

    def clean_password(self):
        """加密密码"""
        password = self.cleaned_data['password']

        return md5(password)

    def clean_confirm_password(self):
        """校验密码"""
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']

        if md5(confirm_password) != password:
            raise ValidationError("两次密码不一致")

        return confirm_password


class LoginForm(BootStrapForm, forms.ModelForm):
    """用户登录校验"""
    email = forms.EmailField(label='邮箱地址')

    password = forms.CharField(label='密码',
                               min_length=8,
                               max_length=32,
                               error_messages={
                                   'min_length': '密码不易太短',
                                   'max_length': '密码不易太长',
                               },
                               widget=forms.PasswordInput())

    class Meta:
        model = UserInfo
        fields = ['email', 'password']

    def clean_email(self):
        """校验邮箱"""
        email = self.cleaned_data['email']

        exists = UserInfo.objects.filter(email=email).exists()
        if not exists:
            raise ValidationError("该邮箱未注册")

        return email

    def clean_password(self):
        """加密密码"""
        password = self.cleaned_data['password']

        return md5(password)


class ModifyPwdForm(BootStrapForm, forms.Form):
    origin_pwd = forms.CharField(label='原密码',
                                 min_length=8,
                                 max_length=32,
                                 error_messages={
                                     'min_length': '密码不易太短',
                                     'max_length': '密码不易太长',
                                 },
                                 widget=forms.PasswordInput())

    new_pwd = forms.CharField(label='新密码',
                              min_length=8,
                              max_length=32,
                              error_messages={
                                  'min_length': '密码不易太短',
                                  'max_length': '密码不易太长',
                              },
                              widget=forms.PasswordInput())

    new_pwd_confirm = forms.CharField(label='再次输入密码',
                                      min_length=8,
                                      max_length=32,
                                      error_messages={
                                          'min_length': '密码不易太短',
                                          'max_length': '密码不易太长',
                                      },
                                      widget=forms.PasswordInput())

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_origin_pwd(self):
        """校验密码，和原密码不一致直接抛出异常"""
        origin_pwd = self.cleaned_data.get('origin_pwd')
        if md5(origin_pwd) != self.request.user.password:
            raise ValidationError("原密码不正确哦")
        return origin_pwd

    def clean_new_pwd(self):
        """加密"""
        return md5(self.cleaned_data['new_pwd'])

    def clean_new_pwd_confirm(self):
        """校验密码"""
        new_pwd = self.cleaned_data['new_pwd']
        new_pwd_confirm = self.cleaned_data['new_pwd_confirm']

        if md5(new_pwd_confirm) != new_pwd:
            raise ValidationError("两次密码不一致")

        return md5(new_pwd_confirm)
