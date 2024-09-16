import os
import time
from urllib.parse import quote

import pygame
import requests

API_KEY = ""
SECRET_KEY = ""


def main(word):
    url = "https://tsn.baidu.com/text2audio"

    text_encode = quote(word)
    mp3_name = f'{word}.mp3'

    if not os.path.exists(mp3_name):
        print('mp3不存在，开始下载')
        payload = f'tex={text_encode}&tok=' + get_access_token() + '&cuid=KcgpxowOfMblvBhgGOsRWYN75N2MhjgB&ctp=1&lan=zh&spd=5&pit=5&vol=5&per=1&aue=3'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            with open(mp3_name, 'wb') as f:
                f.write(response.content)
    else:
        print('mp3已存在无需重复下载')

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load(mp3_name)

    # Play the MP3 file
    for i in range(5):
        pygame.mixer.music.play()

        # Keep the script running until the music is finished
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        time.sleep(2)

    # Clean up
    pygame.mixer.music.unload()


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    with open('dictation.txt', 'r', encoding='utf-8') as f:
        texts = f.readlines()
    for text in texts:
        try:
            main(text.strip())
        except:
            print(text)
            time.sleep(1)
