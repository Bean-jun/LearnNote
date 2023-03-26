import functools
import random
import string
import time

from werkzeug.security import check_password_hash, generate_password_hash


def total_time(f):
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        start = time.time()
        r = f(*args, **kwds)
        print("use time:", time.time()-start)
        return r
    return wrapper


def generate_password(m):
    strs = string.ascii_letters+string.ascii_uppercase + \
        string.ascii_lowercase+string.digits+string.hexdigits
    return "".join([random.choice(strs) for _ in range(m)])


@total_time
def main(password):
    nums = 1024 * 1
    hash_pd = generate_password_hash(password)
    print(password, hash_pd)
    while nums >= 0:
        hash_pd = generate_password_hash(password)
        nums -= 1


if __name__ == "__main__":
    password = generate_password(20)
    main(password)
