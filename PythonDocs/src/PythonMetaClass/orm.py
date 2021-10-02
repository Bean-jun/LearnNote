from .fields import Field, IntField, StringField


class Orm(type):

    def __init__(self, names, bases, dicts):
        super().__init__(names, bases, dicts)

    @staticmethod
    def __new__(cls, names, bases, dicts):
        if names != "Model":
            mapping = {}
            for dic_k, dic_v in dicts.items():
                if isinstance(dic_v, Field):
                    mapping[dic_k] = dic_v

            # 剔除类属性
            for k in mapping:
                dicts.pop(k)

            dicts["__mapping__"] = mapping
            dicts["__tablename__"] = names.lower()

        return type.__new__(cls, names, bases, dicts)


class Model(dict, metaclass=Orm):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self[item]

    def save(self):
        print("save model")

        field = []
        values = []
        for _field, _values in self.__mapping__.items():
            field.append(_field)
            values.append(str(getattr(self, _field, None)))

        sql = "insert into %s (%s) values (%s);" % (self.__tablename__, ','.join(field), ','.join(values))
        print(sql)


class UserInfo(Model):
    username = StringField("username")
    age = IntField("age")


if __name__ == '__main__':
    user = UserInfo(username="张三", age=24)
    user.save()
