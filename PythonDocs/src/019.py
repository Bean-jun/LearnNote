class People():
    def __init__(self, name, age):
        self.name = name
        self.__age = age

    @property
    def age(self):
        # 读取属性
        return self.__age

    @age.setter
    def age(self, val):
        # 设置属性
        self.__age = val

    @age.deleter
    def age(self):
        # 删除属性
        del self.__age


if __name__ == '__main__':
    people = People("小明", 23)
    # 简单多了吧
    people.age += 1
    print(f"{people.name}的年龄是{people.age}")
