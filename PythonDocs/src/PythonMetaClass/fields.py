class Field():

    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return "{} type is {}".format(self.name, self.column_type)


class IntField(Field):

    def __init__(self, name):
        super(IntField, self).__init__(name, "int")


class StringField(Field):

    def __init__(self, name):
        super(StringField, self).__init__(name, "varchar(250)")
