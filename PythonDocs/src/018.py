class People():
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age


if __name__ == '__main__':
    people = People("小明", 23)
    # 简单多了吧
    # people.age += 1  # 试试就知道不行
    print(f"{people.name}的年龄是{people.age}")
