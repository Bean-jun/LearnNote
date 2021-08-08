# 无参函数
def function_1():
    print("这是一个函数")


function_1()


# 有参函数
def function_2(name):
    print(f"大家好，我叫{name}")


function_2("小明")


# 通用参数函数
def function_3(*args, **kwargs):
    print("元组形式:", args)
    print("字典形式:", kwargs)


function_3(1, 2, 3, 4, name="小明", age=23)
