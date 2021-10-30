from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_developer = models.BooleanField(default=False, verbose_name="是否是开发者")
    secret_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="开发者ID")
    secret_value = models.CharField(max_length=200, null=True, blank=True, verbose_name="秘钥")

    class Meta:
        db_table = "User"
