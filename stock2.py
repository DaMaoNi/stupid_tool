import efinance

if __name__ == '__main__':
    performances = efinance.stock.get_all_company_performance()
    for index, row in performances.iterrows():
        stock_code = row.get('股票代码', '未知')
        stock_name = row.get('股票简称', '未知')
        announce_date = row.get('公告日期', '未知')
        revenue_growth = row.get('营业收入同比增长', '未知')
        profit_growth = row.get('净利润同比增长', '未知')
        net_profit = row.get('净利润', '未知')
        condition = net_profit > 0 and profit_growth > revenue_growth > 0
        if condition:
            print(stock_code, stock_name, announce_date, revenue_growth, profit_growth)
