import random

str1 = ""
str2 = ""
for i in range(150):  # 循环150次 每次生成一道题
    num1 = random.randint(0, 99)  # 随机产生数1
    num2 = random.randint(0, 99 - num1)  # 随机产生数2
    symbol = random.choice("+-")
    # 判断符号是加号 还是减号
    if symbol == "+":
        result = num1 + num2  # 是+号 做加法
    else:
        if num1 < num2:
            num1, num2 = num2, num1
        result = num1 - num2  # 否则做减法
    num1 = str(num1).ljust(2, " ")
    num2 = str(num2).ljust(2, " ")
    express1 = num1 + " " + symbol + " " + num2 + " = "
    express2 = num1 + " " + symbol + " " + num2 + " = " + str(result).ljust(2, " ")
    if i % 4 == 3:
        str1 += express1 + "\n"
        str2 += express2 + "\n"
    else:
        str1 += express1 + "\t\t"
        str2 += express2 + "\t\t"
with open("math.txt", "w", encoding="utf8") as file:
    file.write(str1)
with open("key.txt", "w", encoding="utf8") as file:
    file.write(str2)
print("150道100以内加减法混合题试卷:")
print(str1)
print("150道100以内加减法混合题试卷(带答案): ")
print(str2, end="")
print("\033[0m", end="")
