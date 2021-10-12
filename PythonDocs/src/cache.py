import datetime
import json
from functools import wraps, partial

import redis

__all__ = ("cache")

pool = redis.ConnectionPool(host='localhost', port=6379, db=15)


class DB():
    def __init__(self, exp, db_type="default"):
        self.exp = exp  # 过期时间
        if db_type == "redis":
            import redis
            self.db = redis.Redis(connection_pool=pool)
        elif db_type == "default":
            self.db = {}

    def set(self, key, value):
        if isinstance(self.db, redis.Redis):
            self.db.setex(name=key, value=value, time=self.exp)
        else:
            self.db[key] = value

    def get(self, key):
        if isinstance(self.db, redis.Redis):
            try:
                ret = self.db.get(key).decode()
                ret = json.loads(ret)
            except Exception as e:
                return None
            else:
                return ret
        else:
            return self.db.get(key)

    def pop(self, key):
        if isinstance(self.db, redis.Redis):
            self.db.delete(key)
        else:
            self.db.pop(key)

    def clear(self):
        pass


def _cache(exp, prefix="", request=None):
    """
    exp: 过期时间(单位：秒)
    """
    try:
        db = DB(exp, "redis")
    except Exception as e:
        db = DB(exp, "default")

    def cache_func(f):
        @wraps(f)
        def inner(*args, **kwargs):
            nonlocal prefix

            if not prefix:
                prefix = "Cache"

            try:
                k_fmt = "{}:{}-{}".format(prefix, f.__name__, request.full_path)
            except Exception as e:
                k_fmt = "{}:{}-{}".format(prefix, f.__name__, None)

            cache_ret = db.get(k_fmt)

            if cache_ret:
                if datetime.datetime.strptime(cache_ret.get("create"), "%Y-%m-%d %H:%M%S") + datetime.timedelta(
                        seconds=exp) < datetime.datetime.now():
                    # 数据过期
                    db.pop(k_fmt)
                else:
                    return json.loads(cache_ret["val"])

            ret = f(*args, **kwargs)

            db.set(k_fmt, json.dumps({
                "val": json.dumps(ret),
                "exp": exp,
                "create": datetime.datetime.now().strftime("%Y-%m-%d %H:%M%S")
            }))
            return ret

        return inner

    return cache_func


try:
    from flask import request

    cache = partial(_cache, request=request)
except Exception as e:
    print("请安装flask环境")
