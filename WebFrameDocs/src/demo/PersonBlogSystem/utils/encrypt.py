from django.conf import settings
import hashlib
import random
import uuid


def md5(string):
    # md5 加密
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(string.encode('utf-8'))

    return obj.hexdigest()


def add_salt(string):
    """处理数据加盐"""
    _ = [i + str(random.randint(0, 9)) for i in string]
    res = "".join(_)
    return res


def decr_salt(string):
    """处理数据减盐"""
    _ = [data for i, data in enumerate(string) if i % 2 == 0]
    res = "".join(_)
    return res


def file_uid(value):
    """文件名"""
    _uid = "{}666{}".format(str(uuid.uuid4()), value)
    return md5(_uid)


def uid(value):
    """邀请链接"""
    _uid = "{}-{}".format(str(uuid.uuid4()), value)
    return md5(_uid)
