import efinance
import pandas as pd

if __name__ == '__main__':
    performances = efinance.stock.get_all_company_performance()

    # 创建一个列表用于临时存储符合条件的数据
    result_data = []

    for index, row in performances.iterrows():
        stock_code = row.get('股票代码', '未知')
        stock_name = row.get('股票简称', '未知')
        announce_date = row.get('公告日期', '未知')
        revenue_growth = row.get('营业收入同比增长', '未知')
        profit_growth = row.get('净利润同比增长', '未知')
        net_profit = row.get('净利润', '未知')
        condition = net_profit > 0 and profit_growth > revenue_growth > 0
        if condition:
            market_value = efinance.stock.get_latest_quote(stock_code).get('总市值')[0]
            if market_value < 100000000000:
                continue
            print(stock_code, stock_name, announce_date, revenue_growth, profit_growth, net_profit, market_value)

            # 新增：将符合条件的数据添加到结果列表
            result_data.append({
                '股票代码': stock_code,
                '股票简称': stock_name,
                '公告日期': announce_date,
                '营业收入同比增长': revenue_growth,
                '净利润同比增长': profit_growth,
                '净利润': net_profit,
                '总市值': market_value
            })

    # 新增：将结果保存为 Excel 文件
    if result_data:
        result_data.sort(key=lambda x: x['总市值'], reverse=True)
        try:
            result_df = pd.DataFrame(result_data)
            result_df.to_excel('上市公司业绩表现.xlsx', index=False)
            print(f"\n已成功将结果保存到 '上市公司业绩表现.xlsx' 文件中")
        except Exception as e:
            print(f"保存 Excel 文件时出错: {e}")
    else:
        print("\n没有找到符合条件的公司数据")
