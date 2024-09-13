import pyttsx3

CNT = 10

if __name__ == '__main__':
    # 初始化TTS引擎
    engine = pyttsx3.init()

    # 设置要报听写的文本
    with open('dictation.txt', 'r', encoding='utf-8') as f:
        texts = f.readlines()

    # 设置语速，可选，可以根据需要调整
    # 值越小语速越慢，值越大语速越快
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 50)

    # 将文本添加到TTS引擎
    for text in texts:
        for i in range(CNT):
            engine.say(text)

    # 等待所有当前任务完成
    engine.runAndWait()
