import os

moviePath = r"E:\jellyfin\data"
for item in os.walk(moviePath):
    if item[0] == moviePath:
        for file in item[2]:
            if file.endswith(".torrent"):
                continue
            filePath = item[0] + "\\" + file
            dirPath = os.path.splitext(filePath)[0]
            if not os.path.exists(dirPath):
                os.mkdir(dirPath)
            os.replace(filePath, dirPath + "\\" + file)
