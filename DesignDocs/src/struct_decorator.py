# 修饰器模式
import time
import functools

def memoize(f):
    cache_dict = {}
    @functools.wraps(f)
    def wrapper(*args):
        if args not in cache_dict:
            cache_dict[args] = f(*args)
        return cache_dict[args]
    return wrapper


@memoize    # 语法糖  对于一些其他语言，可以这样  fibo = memoize(fibo)
def fibo(n):
    if n < 2:
        return 1
    return fibo(n-1) + fibo(n-2)


if __name__ == "__main__":
    t1 = time.time()
    ret = fibo(40)
    print(f"ret: {ret} use time: {time.time() - t1}")