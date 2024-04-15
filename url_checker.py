import re

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

FILE_PATH = r'E:\jellyfin\iptv\test.m3u'


def check_url(url):
    try:
        return requests.get(url, timeout=3, verify=False).status_code == 200
    except:
        return False


def check():
    pattern = re.compile('(?<!")https?://.*')
    count_ok = 0
    count_nok = 0
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
        tmp = pattern.findall(content)
        for item in tmp:
            if check_url(item):
                count_ok += 1
            else:
                count_nok += 1
                print('[nok]%s' % item)
    print('count_ok:%d' % count_ok)
    print('count_nok:%d' % count_nok)
    print('success rate', round(count_ok / (count_ok + count_nok) * 100, 1), '%')


if __name__ == "__main__":
    check()
