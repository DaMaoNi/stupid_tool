import random
import os


def generate_divison_wo_remainder():
    """生成无余数的除法题目"""
    while True:
        divisor = random.randint(2, 9)
        quotient = random.randint(10, 99)
        dividend = divisor * quotient
        if dividend <= 999:
            return f"{dividend} ÷ {divisor} = "


def generate_divison_w_remainder():
    """生成有余数的除法题目"""
    while True:
        divisor = random.randint(2, 9)
        quotient = random.randint(10, 99)
        remainder = random.randint(1, divisor - 1)
        dividend = divisor * quotient + remainder
        if dividend <= 999:
            return f"{dividend} ÷ {divisor} = "


def generate_expression():
    """生成脱式计算题（三个数，两种运算）"""
    operations = ['+', '-', '×', '÷']
    # 确保有足够的空间进行运算，避免过小的数字
    num1 = random.randint(2, 99)
    num2 = random.randint(2, 99)
    num3 = random.randint(2, 99)

    # 随机选择两个运算符
    op1 = random.choice(operations)
    op2 = random.choice(operations)

    # 避免连续除法导致小数
    if op1 == '÷':
        # 确保num1能被num2整除
        num1 = num2 * random.randint(1, 10)
    if op2 == '÷':
        # 确保前两个数运算结果能被num3整除
        if op1 in ['+', '-']:
            # 调整num3，使其能整除前两个数的结果
            temp = num1 + num2 if op1 == '+' else num1 - num2
            if temp != 0:
                factors = [i for i in range(2, abs(temp) + 1) if temp % i == 0]
                if factors:
                    num3 = random.choice(factors)
                else:
                    num3 = 1
        elif op1 == '×':
            # 确保num1*num2能被num3整除
            product = num1 * num2
            if product != 0:
                factors = [i for i in range(2, abs(product) + 1) if product % i == 0]
                if factors:
                    num3 = random.choice(factors)
                else:
                    num3 = 1

    return f"{num1} {op1} {num2} {op2} {num3}"


def create_exercises():
    """创建练习题集"""
    # 生成题目
    division_wo_remainder = [generate_divison_wo_remainder() for _ in range(20)]
    division_w_remainder = [generate_divison_w_remainder() for _ in range(20)]
    expressions = [generate_expression() for _ in range(20)]

    # 创建输出目录
    if not os.path.exists('math_exercises'):
        os.makedirs('math_exercises')

    # 输出到同一个文本文件
    with open('math_exercises/all_exercises.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 20 + " 无余数除法 " + "=" * 20 + "\n\n")
        for i, problem in enumerate(division_wo_remainder, 1):
            f.write(f"{i}. {problem}\n\n\n\n")  # 留出答题空间

        f.write("\n\n" + "=" * 20 + " 有余数除法 " + "=" * 20 + "\n\n")
        for i, problem in enumerate(division_w_remainder, 1):
            f.write(f"{i}. {problem}\n\n\n\n")  # 留出答题空间

        f.write("\n\n" + "=" * 20 + " 脱式计算题 " + "=" * 20 + "\n\n")
        for i, problem in enumerate(expressions, 1):
            f.write(f"{i}. {problem}\n\n\n\n")  # 留出答题空间

    print("练习题已生成到'math_exercises/all_exercises.txt'")


if __name__ == "__main__":
    create_exercises()