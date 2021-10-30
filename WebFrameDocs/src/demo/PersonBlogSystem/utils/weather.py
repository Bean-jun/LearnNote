# -*- encoding: utf-8 -*-
"""
获取天气模块
"""
import re
import json
import time
import requests

headers = {
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42'
}


def _set_url(city):
    """获取当前地址的页面戳"""
    _ = str(time.time() * 1000)[1:].split('.')[0]
    url = f"http://toy1.weather.com.cn/search?cityname={city}&callback=success_jsonpCallback&_={_}"
    try:
        response = requests.get(url, headers=headers)
    except Exception as e:
        pass
    else:
        code = re.findall('(\d+)~', response.text)
        if code is not None:
            return code[0]
        return False


def get_weather(city):
    """获取天气"""
    res = _set_url(city)
    if not res:
        return None
    else:
        _ = str(time.time() * 1000).split('.')[0]
        url = f"http://d1.weather.com.cn/sk_2d/{res}.html?_={_}"
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            pass
        else:
            _ = response.content.decode('utf-8')
            data = json.loads(_.split("=")[1])
            return data


if __name__ == '__main__':
    get_weather("武汉")
