"""
文件存储对象名称调整
"""
import random
import uuid
from datetime import datetime

from utils.scale_num import ScaleNum

scale = ScaleNum()


def save_facker_name(filename: str):
    '''
    文件名称转换器
    '''
    try:
        file_type = filename.rsplit('.', 1)[-1]
    except Exception as e:
        file_type = ""

    now = datetime.now()
    str_num = ''
    for t in [now.year, now.month, now.day, now.hour, now.minute, now.second]:
        str_num += str(t)

    str_num += str(10000*int(random.random()))

    facker_name = scale.to_scale(int(str_num))
    facker_name += ".{}".format(file_type)

    return facker_name


def save_facker_name_plus(filename: save_facker_name):
    try:
        file_type = filename.rsplit('.', 1)[-1]
        filename = filename.rsplit('.', 1)[0]
    except Exception as e:
        file_type = ""

    uid = str(uuid.uuid4())
    facker_name = filename + "-" + uid + ".{}".format(file_type)

    return facker_name


if __name__ == "__main__":
    name = save_facker_name("sdaf.png")
    new_name = save_facker_name_plus(name)
    print(name, new_name)
