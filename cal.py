import random

directions = ['+', '-', 'x']

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def generate_pdf(string_list, filename='output.pdf'):
    """
    生成一个包含字符串列表的PDF文件。

    :param string_list: 要写入PDF的字符串列表
    :param filename: 输出PDF文件的名称，默认为'output.pdf'
    """
    # 创建一个PDF画布
    c = canvas.Canvas(filename, pagesize=letter)

    # 设置初始y坐标
    y = 750
    x = 72
    n = 6
    for string in string_list:
        # 将字符串写入PDF
        c.drawString(x, y, string)
        # 每次写入后，y坐标向下移动20个单位
        y -= 20
        if y < 0:
            y = 750
            x += 72
            n -= 1
            if n == 0:
                break

    # 保存PDF文件
    c.save()


def random_element(max):
    return random.randint(0, max)


def main(res):
    global directions
    direction = directions[random_element(2)]
    if direction == '+':
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        r = a + b
        if r <= 100:
            res.append(f'{a}+{b}={r}')
    elif direction == '-':
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        r = a - b
        if r >= 0:
            res.append(f'{a}-{b}={r}')
    else:
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        r = a * b
        res.append(f'{a}x{b}={r}')


if __name__ == '__main__':
    res = set()
    for i in range(1000):
        main(res)
    generate_pdf(res)
