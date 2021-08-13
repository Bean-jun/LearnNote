class People():
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def name(self):
        return self.__name

    def age(self):
        return self.__age


if __name__ == '__main__':
    people = People("小明", 23)
    try:
        print(f"{people.__name}的年龄是{people.__age}")
    except Exception as e:
        print(e.args)
    # 哦豁~，好像没法正常访问哎~那我们怎么办呢
    # 1. 直接访问 对于私有属性可以使用    对象._类名__属性  不推荐
    print(f"{people._People__name}的年龄是{people._People__age}")
    # 2. 定义方法去访问
    print(f"{people.name()}的年龄是{people.age()}")
