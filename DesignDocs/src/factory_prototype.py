import copy


class User():

    def __init__(self, id, name, age, gender):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender

    def __str__(self):
        return "%s-%s-%s-%s" % (self.id, self.name, self.age, self.gender)


class Prototype():

    def __init__(self):
        self.obj = dict()

    def register(self, identify, obj):
        self.obj[identify] = obj

    def unregister(self, identify):
        del self.obj[identify]

    def clone(self, identify, **attrs):
        found_obj = self.obj.get(identify)
        if not found_obj:
            raise
        obj = copy.deepcopy(found_obj)
        obj.__dict__.update(attrs)
        return obj


if __name__ == "__main__":
    data01 = User("1", "张三", 20, "男")
    print(data01)

    prototype = Prototype()
    identify = "data001"
    prototype.register(identify, data01)
    data02 = prototype.clone(identify, **{
        "id": 2,
        "name": "李四",
        "age": 22,
        "gender": "男",
    })
    print(data01, data02, id(data01), id(data02))
