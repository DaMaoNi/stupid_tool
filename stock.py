import random
import string

import efinance
import requests

TEST = False


def generate_random_number_string(length=18):
    return ''.join(random.choices(string.digits, k=length))


def cal_profit(stock_code):
    random_string = generate_random_number_string()
    url = f'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_F10_FINANCE_MAINFINADATA&sty=APP_F10_MAINFINADATA&quoteColumns=&filter=(SECUCODE%3D%22{stock_code}%22)&p=1&ps=9&sr=-1&st=REPORT_DATE&source=HSF10&client=PC&v={random_string}'
    response = requests.get(url)
    if response.status_code == 200:
        res = response.json()
        datas = res.get('result').get('data')
        if len(datas) == 0:
            return 0
        elif len(datas) == 1 or datas[0].get('REPORT_TYPE') == '一季报':
            return datas[0].get('KCFJCXSYJLR')
        else:
            return datas[0].get('KCFJCXSYJLR') - datas[1].get('KCFJCXSYJLR')


def get_market_value(stock_code):
    return efinance.stock.get_latest_quote(stock_code).get('总市值')[0]


def get_pe(stock_code):
    return efinance.stock.get_latest_quote(stock_code).get('动态市盈率')[0]


def get_value(stock_code):
    res = 'error'
    try:
        return get_market_value(stock_code) / cal_profit(stock_code + '.SH') / 4
    except:
        pass

    try:
        return get_market_value(stock_code) / cal_profit(stock_code + '.SZ') / 4
    except:
        pass

    try:
        return get_market_value(stock_code) / cal_profit(stock_code + '.BJ') / 4
    except:
        pass
    return res


def judge(tmp_code):
    global TEST
    try:
        value = get_value(tmp_code)
        pe = get_pe(tmp_code)
        if value == 'error':
            print(f'{stock_code} error.')
        elif pe < 0 < value <= 20:
            print(f'{stock_code} omg!!!value:{value},pe:{pe}')
        elif TEST:
            print(f'{stock_code} omg!!!value:{value},pe:{pe}')
    except Exception as e:
        print(f'{stock_code} error!!!')
        print(e)


if __name__ == '__main__':
    stock_codes = []
    if len(stock_codes) == 0:
        stock_codes = efinance.stock.get_all_company_performance().get('股票代码')
    else:
        TEST = True
    for stock_code in stock_codes:
        judge(stock_code)
    print('done!')
