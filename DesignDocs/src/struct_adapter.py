# 适配器模式
class Charge:
    """标准充电器"""

    def start(self):
        print(f"标准充电器, 为iPhone充电中")
    
class ChineseCharge:
    """国行充电器"""

    def charge5V(self):
        print("国行5v充电器，为iPhone充电中")


class OtherCharge:
    """其他充电器"""

    def super_charge(self):
        print("其他超级快充充电器，为iPhone充电中")


class AdapterCharge:
    """转换器，为充电器适配"""
    def __init__(self, charge, *args, **kwargs):
        self.__charge = charge(*args, **kwargs)
        if isinstance(self.__charge, Charge):
            self.__charge.do_charge = self.__charge.start
        if isinstance(self.__charge, ChineseCharge):
            self.__charge.do_charge = self.__charge.charge5V
        if isinstance(self.__charge, OtherCharge):
            self.__charge.do_charge = self.__charge.super_charge
    
    def execute(self, *args, **kwargs):
        self.__charge.do_charge(*args, **kwargs)


if __name__ == "__main__":
    adapter1 = AdapterCharge(Charge)
    adapter1.execute()
    adapter2 = AdapterCharge(ChineseCharge)
    adapter2.execute()
    adapter3 = AdapterCharge(OtherCharge)
    adapter3.execute()