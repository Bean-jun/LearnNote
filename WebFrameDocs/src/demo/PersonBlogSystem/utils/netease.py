import re
import requests


headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.42'
}


def match_id(url):
    """匹配歌单ID"""
    try:
        res = re.findall('id=(\d{4,12})', url)
        return res[0]
    except Exception as e:
        pass

    return None


def match_title(url):
    """匹配歌单标题"""
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        else:
            res = re.search('<title>.+', response.text).group()
            title = res.strip('<title>').split(' -')[0]
            return title
    except Exception as e:
        pass

    return None
