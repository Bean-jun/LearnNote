from django import forms
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm

from Auth.models import User


class UserRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def __init__(self, request, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_username(self):
        username = self.cleaned_data["username"]
        exists = User.objects.filter(username=username).exists()
        if exists:
            self.request.error = {"msg": "用户名已注册"}
            raise ValidationError("用户名已注册")

        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        exists = User.objects.filter(email=email).exists()
        if exists:
            self.request.error = {"msg": "邮箱已注册"}
            raise ValidationError("邮箱已注册")

        return email

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        password = make_password(pwd, None, "pbkdf2_sha256")
        return password


class UserLoginForm(ModelForm):
    username = forms.CharField(
        max_length=150,
        required=False,
        validators=[UnicodeUsernameValidator()],
    )
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def __init__(self, request, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        pwd = self.cleaned_data.get("password")

        user = User.objects.filter(
            Q(username=username) | Q(email=username) | Q(email=username) | Q(email=email)
        ).first()

        if not user:
            self.request.error = {"msg": "用户不存在"}
            raise ValidationError("用户不存在")

        if not check_password(pwd, user.password):
            self.request.error = {"msg": "账号密码错误"}
            raise ValidationError("账号密码错误")

        self.cleaned_data["inner_user"] = user

        return self.cleaned_data
