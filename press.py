import ctypes
import os
import signal
import sys
import time
import tkinter as tk

import pygetwindow as gw

try:
    root = os.path.abspath(os.path.dirname(__file__))
    # driver = ctypes.CDLL(os.path.join(os.path.dirname(os.path.realpath(sys.executable)), 'logitech.driver.dll'))
    driver = ctypes.CDLL(r'C:\Users\admin\Desktop\press\logitech.driver.dll')
    ok = driver.device_open() == 1  # 该驱动每个进程可打开一个实例
    if not ok:
        print('Error, GHUB or LGS driver not found')
except FileNotFoundError:
    print(f'Error, DLL file not found')
    sys.exit(1)

running = False
F = False


class Logitech:
    class mouse:

        """
        code: 1:左键, 2:中键, 3:右键
        """

        @staticmethod
        def press(code):
            if not ok:
                return
            driver.mouse_down(code)

        @staticmethod
        def release(code):
            if not ok:
                return
            driver.mouse_up(code)

        @staticmethod
        def click(code):
            if not ok:
                return
            driver.mouse_down(code)
            driver.mouse_up(code)

        @staticmethod
        def scroll(a):
            """
            a:没搞明白
            """
            if not ok:
                return
            driver.scroll(a)

        @staticmethod
        def move(x, y):
            """
            相对移动, 绝对移动需配合 pywin32 的 win32gui 中的 GetCursorPos 计算位置
            pip install pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple
            x: 水平移动的方向和距离, 正数向右, 负数向左
            y: 垂直移动的方向和距离
            """
            if not ok:
                return
            if x == 0 and y == 0:
                return
            driver.moveR(x, y, False)

    class keyboard:

        """
        键盘按键函数中，传入的参数采用的是键盘按键对应的键码
        code: 'a'-'z':A键-Z键, '0'-'9':0-9, 其他的没猜出来
        """

        @staticmethod
        def press(code):

            if not ok:
                return
            driver.key_down(code)

        @staticmethod
        def release(code):
            if not ok:
                return
            driver.key_up(code)

        @staticmethod
        def click(code):
            if not ok:
                return
            driver.key_down(code)
            driver.key_up(code)


def cleanup():
    Logitech.keyboard.release('2')
    Logitech.keyboard.release('1')
    print('退出成功')


def task():
    global running
    while True:
        try:
            # 获取当前活动窗口
            active_window = gw.getActiveWindow()
            if running and not F and active_window.title.find('塔瑞斯世界') != -1:
                Logitech.keyboard.press('2')
                Logitech.keyboard.release('2')
                Logitech.keyboard.press('1')
                Logitech.keyboard.release('1')
                time.sleep(0.1)
            elif running and F and active_window.title.find('塔瑞斯世界') != -1:
                Logitech.keyboard.press('f')
                Logitech.keyboard.release('f')
                time.sleep(0.1)
            else:
                time.sleep(1)
        except:
            pass


def signal_handler(signum, frame):
    print("接收到信号，准备退出")
    cleanup()
    sys.exit(1)


# 点击开始按钮时执行的函数
def on_start_button_click():
    global running
    global F
    running = True
    F = False


# 点击结束按钮时执行的函数
def on_stop_button_click():
    global running
    global F
    running = False
    F = False


def on_F_button_click():
    global running
    global F
    running = True
    F = True


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

import threading

# 创建线程对象，指定要执行的函数
thread = threading.Thread(target=task)

# 启动线程
thread.start()


def close():
    os.kill(os.getpid(), signal.SIGINT)


def MouseDown(event):  # 不要忘记写参数event
    global mousX  # 全局变量，鼠标在窗体内的x坐标
    global mousY  # 全局变量，鼠标在窗体内的y坐标

    mousX = event.x  # 获取鼠标相对于窗体左上角的X坐标
    mousY = event.y  # 获取鼠标相对于窗左上角体的Y坐标


def MouseMove(event):
    root.geometry(f'+{event.x_root - mousX}+{event.y_root - mousY}')  # 窗体移动代码
    # event.x_root 为窗体相对于屏幕左上角的X坐标
    # event.y_root 为窗体相对于屏幕左上角的Y坐标


if __name__ == '__main__':  # 测试
    # 创建主窗口
    root = tk.Tk()
    root.title("Press")
    root.resizable(False, False)
    root.attributes('-topmost', 'true')
    root.attributes("-toolwindow", True)
    root.state('normal')
    root.protocol("WM_DELETE_WINDOW", close)
    # root.bind("<Button-1>", MouseDown)  # 按下鼠标左键绑定MouseDown函数
    # root.bind("<B1-Motion>", MouseMove)  # 鼠标左键按住拖曳事件,3个函数都不要忘记函数写参数

    # 创建开始按钮，并添加到主窗口
    start_button = tk.Button(root, text="Start", command=on_start_button_click)
    start_button.pack(side=tk.LEFT, padx=10, pady=10)

    # 创建结束按钮，并添加到主窗口
    stop_button = tk.Button(root, text="Stop", command=on_stop_button_click)
    stop_button.pack(side=tk.RIGHT, padx=10, pady=10)

    stop_button = tk.Button(root, text="F", command=on_F_button_click)
    stop_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    # 运行主事件循环
    root.mainloop()
