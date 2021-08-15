from contextlib import contextmanager


@contextmanager
def func():
    print("我又开始了~")
    try:
        yield 1
    finally:
        print("完事了~, 看")


if __name__ == '__main__':
    with func() as f:
        print(f)
