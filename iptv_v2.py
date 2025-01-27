import sys
import json
from urllib.request import urlopen
from datetime import datetime
from threading import Thread
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 硬编码配置参数
CHANNEL_INFO_URL = "http://111.20.43.97:29010/chnInfos/SAXYD_ZX/0.json"
EPG_LIST_URL = "http://111.20.43.97:29010/tagNewestEpgList/SAXYD_ZX/1/100/0.json"
UPDATE_INTERVAL = 3600  # 单位：秒 (1小时)
SERVER_ADDRESS = ("0.0.0.0", 8000)  # 监听地址和端口


class UpdateFilesThread(Thread):
    def __init__(self):
        super().__init__(daemon=True, name="EPG-Updater")

    def generate_m3u(self, channels):
        """生成M3U文件内容"""
        header = '#EXTM3U x-tvg-url="gitv.xml"\n'
        return header + "\n".join(
            f'#EXTINF:-1 tvg-id="{ch["tvg_id"]}" tvg-name="{ch["tvg_name"]}" '
            f'tvg-logo="{ch["tvg_logo"]}" group-title="{ch["group_title"]}",{ch["tvg_name"]}\n'
            f'{ch["m3u8"]}'
            for ch in channels
        )

    def generate_xmltv(self, channels):
        """生成XMLTV文件内容"""
        xml = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<!DOCTYPE tv SYSTEM "xmltv.dtd">',
            '<tv source-info-name="GITV EPG">'
        ]

        # 添加频道定义
        xml.extend(
            f'<channel id="{ch["channel_id"]}">'
            f'<display-name>{ch["display_name"]}</display-name>'
            '</channel>'
            for ch in channels
        )

        # 添加节目单
        xml.extend(
            f'<programme start="{ch["programme_start"]}" stop="{ch["programme_stop"]}" channel="{ch["channel_id"]}">'
            f'<title lang="zh">{ch["programme_title"]}</title>'
            '</programme>'
            for ch in channels
        )

        xml.append('</tv>')
        return '\n'.join(xml)

    def run(self):
        while True:
            try:
                print("[EPG] 开始更新频道数据...")
                start_time = time.time()

                # 获取频道元数据
                with urlopen(CHANNEL_INFO_URL) as resp:
                    channel_info = json.loads(resp.read().decode())["data"]

                # 获取EPG数据
                with urlopen(EPG_LIST_URL) as resp:
                    epg_data = json.loads(resp.read().decode())["data"]

                # 构建图标映射表
                icon_mapping = {ch["chnCode"]: ch["bigChnIcon"] for ch in channel_info}

                # 加载播放地址缓存
                try:
                    with open("cache.json") as f:
                        cache = json.load(f)
                except FileNotFoundError:
                    cache = {}

                # 处理频道数据
                processed = 0
                m3u_channels = []
                xmltv_channels = []

                for channel in epg_data:
                    chn_code = channel["chnCode"]

                    # 获取播放地址
                    if chn_code not in cache:
                        with urlopen(channel["playUrl"]) as resp:
                            cache[chn_code] = {"m3u8": json.loads(resp.read().decode())["u"]}

                    # M3U数据
                    m3u_channels.append({
                        "tvg_id": chn_code,
                        "tvg_name": channel["chnName"],
                        "tvg_logo": icon_mapping.get(chn_code, ""),
                        "group_title": "GITV",
                        "m3u8": cache[chn_code]["m3u8"]
                    })

                    # XMLTV数据
                    xmltv_channels.append({
                        "channel_id": chn_code,
                        "display_name": channel["chnName"],
                        "programme_title": channel["title"],
                        "programme_start": datetime.fromtimestamp(channel["startTime"] / 1000).strftime(
                            "%Y%m%d%H%M%S +0800"),
                        "programme_stop": datetime.fromtimestamp(channel["endTime"] / 1000).strftime(
                            "%Y%m%d%H%M%S +0800")
                    })

                    processed += 1
                    if processed % 10 == 0:
                        print(f"[EPG] 已处理 {processed} 个频道...")

                # 生成文件
                with open("gitv.m3u", "w", encoding="utf-8") as f:
                    f.write(self.generate_m3u(m3u_channels))

                with open("gitv.xml", "w", encoding="utf-8") as f:
                    f.write(self.generate_xmltv(xmltv_channels))

                # 保存缓存
                with open("cache.json", "w") as f:
                    json.dump(cache, f)

                cost = time.time() - start_time
                print(f"[EPG] 更新完成！共处理 {processed} 个频道，耗时 {cost:.2f} 秒")
                time.sleep(UPDATE_INTERVAL)

            except Exception as e:
                print(f"[ERROR] 更新失败: {str(e)}")
                time.sleep(300)  # 错误时等待5分钟重试


class HttpServerThread(Thread):
    def __init__(self):
        super().__init__(daemon=True, name="HTTP-Server")

    def run(self):
        server = HTTPServer(SERVER_ADDRESS, SimpleHTTPRequestHandler)
        print(f"[HTTP] 服务器已启动 http://{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}")
        server.serve_forever()


def main():
    UpdateFilesThread().start()
    HttpServerThread().start()
    try:
        while True: time.sleep(3600)
    except KeyboardInterrupt:
        print("\n服务已停止")


if __name__ == '__main__':
    main()