import requests


def txt_to_m3u(txt_file_path, m3u_file_path):
    """
    将TXT文件中的音频文件路径转换为M3U播放列表。

    参数:
    txt_file_path (str): TXT文件的路径。
    m3u_file_path (str): 输出的M3U文件的路径。
    """
    try:
        # 打开TXT文件并读取内容
        with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
            lines = txt_file.readlines()

        # 打开M3U文件准备写入
        with open(m3u_file_path, 'w', encoding='utf-8') as m3u_file:
            # 写入M3U文件头
            m3u_file.write('#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml"\n')

            # 遍历每一行，写入M3U文件
            for line in lines:
                if 'http' in line:
                    line_arr = line.split(',')
                    # 去除行尾的换行符并写入
                    m3u_file.write(f'#EXTINF:-1,{line_arr[0]}\n')
                    m3u_file.write(line_arr[1])

        print(f"转换完成，M3U文件已保存至：{m3u_file_path}")
    except Exception as e:
        print(f"转换过程中发生错误：{e}")


if __name__ == '__main__':
    txt_file_path = 'txt_file_path'
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        text = requests.get('https://fanmingming.com/txt?url=https://live.fanmingming.com/tv/m3u/ipv6.m3u', timeout=30).text
        txt_file.write(text)

    m3u_file_path = r'test.m3u'  # 替换为你希望保存M3U文件的路径
    txt_to_m3u(txt_file_path, m3u_file_path)
