import json

import requests

TEST_URL = '/udp/239.254.96.96:8550'

if __name__ == "__main__":
    data = []
    with open('测绘.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    total = len(data)
    i = 0
    with open('iptv_result.txt', 'w', encoding='utf-8') as f:
        for item in data:
            try:
                url = item["URL"]
                iptv_url = f'{url}{TEST_URL}'
                i += 1
                print(f'{i}/{total}')
                stream_response = requests.get(iptv_url, stream=True, timeout=3)
                chunk = next(stream_response.iter_content(chunk_size=1024))
                if chunk:
                    print(iptv_url)
                    f.write(iptv_url)
                    f.write('\n')
            except:
                pass
