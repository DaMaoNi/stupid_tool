"""
根据贷款金额、分期数、月供反推贷款利率，避免被银行坑
"""
import sys

a = 20000  # 贷款金额
n = 12  # 期数
r = 1700  # 月供
h = sys.maxsize  # 利率上限
l = 0  # 利率下限


def cal_interest(a, i, n):
    j = i / 12
    return a * j * (1 + j) ** n / ((1 + j) ** n - 1)


def helper(l, h):
    m = l + (h - l) / 2
    tmp = cal_interest(a, m, n)
    if abs(tmp - r) < 0.01:
        return m
    elif tmp > r:
        return helper(l, m)
    else:
        return helper(m, h)


if __name__ == '__main__':
    print(f'年利率：{round(helper(l, h) * 100, 1)}%')
