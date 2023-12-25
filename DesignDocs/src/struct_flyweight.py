# 享元模式
from abc import ABCMeta

class Car(metaclass=ABCMeta):
    name = "car"

class MiniCar(Car):
    name = "MiniCar"

class BusCar(Car):
    name = "BusCar"

class BigCar(Car):
    name = "BigCar"

class CreateCar:
    pool = dict()

    def __init__(self, car: Car):
        self.car = car

    def __new__(cls, car: Car, *args, **kwargs):
        _car = cls.pool.get(car.name)
        if not _car:
            _car = object.__new__(cls)
            cls.pool[car.name] = _car
        return _car
    
    def numberid(self):
        return id(self.car)

if __name__ == "__main__":
    mini_car = MiniCar()
    bus_car = BusCar()
    big_car = BigCar()
    # 对象已创建，即使不停创建的实例，都是基于此对象进行创建
    for _ in range(10):
        c1 = CreateCar(mini_car)
        print(f"{c1.car.name} car id {c1.numberid()}")
    for _ in range(10):
        c2 = CreateCar(bus_car)
        print(f"{c2.car.name} car id {c2.numberid()}")
    for _ in range(10):
        c3 = CreateCar(big_car)
        print(f"{c3.car.name} car id {c3.numberid()}")
    for _ in range(10):
        c4 = CreateCar(mini_car)
        print(f"{c4.car.name} car id {c4.numberid()}")
