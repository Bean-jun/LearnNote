from django.db import models


class UserInfoWeiBo(models.Model):
    """微博用户"""
    user = models.OneToOneField("blog.UserInfo", on_delete=models.CASCADE, verbose_name="用户")
    access_token = models.CharField(max_length=128, verbose_name="授权码")
    expires = models.CharField(max_length=32, verbose_name="过期时间")
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    modify_datetime = models.DateTimeField(auto_now=True, verbose_name="修改时间")
