"""
62进制定义：
0-9, A-Z, a-z 组合

本工具将十进制数字转换为62进制数字
"""
from utils.common import ScaleMap


class ScaleNum():
    """
    一个普通的十进制转其他进制的进制转换器 
    2进制到62位进制内可以任意转换
    """

    def __init__(self, scale=62) -> None:
        self.scale = scale

    def to_scale(self, num):
        self._ret = []
        while True:
            num, temp = divmod(num, self.scale)
            self._ret.append(temp)

            if num < self.scale:
                self._ret.append(num)
                break

        self._ret.reverse()
        self._new_ret = []
        for n in self._ret:
            if n in ScaleMap:
                self._new_ret.append(ScaleMap[n])
            else:
                self._new_ret.append(str(n))

        return "".join(self._new_ret)


if __name__ == "__main__":
    r = ScaleNum()
    ret = r.to_scale(317547456780234234)
    print(ret)
