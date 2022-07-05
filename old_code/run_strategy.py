import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as py

from strategies.GoldenCross import GoldenCross

back_test_stock_csv = 'AAPL'
stock_data_path = '.\\stock_price_csv\\{}.csv'.format(back_test_stock_csv)
csv_path = stock_data_path


if __name__ == "__main__":
    # 開啓backtrader的cerebro (大腦)
    cerebro = bt.Cerebro()
    # 讀取csv
    #df = pd.read_csv('../stock_price_csv/{}.csv'.format(back_test_stock_csv))
    df = pd.read_csv(csv_path)
    
    # 改變csv 內包含的日期格式
    df['Datetime'] = pd.to_datetime(df['Date'])
    # 把Datetime改變為index
    df.set_index('Datetime', inplace=True)

    # 設定名字, 回測日期段, 回測時間段, 把設定好的data加入cerebro (大腦).
    data_stock = bt.feeds.PandasData( dataname = df, fromdate = dt.datetime(2021, 12, 1), todate = dt.datetime(2022, 6, 30), timeframe = bt.TimeFrame.Days)
    cerebro.adddata(data_stock)

    # 把上邊的策略載入cerebro (大腦)
    cerebro.addstrategy(GoldenCross)

    # 載入分析器 - 夏普比率
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name = 'SharpeRatio') 
    # 載入分析器 - 最大跌幅
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name = 'DrawDown')

    # 開始資金
    cerebro.broker.setcash(10000.0)
    # 交易所佣金
    cerebro.broker.setcommission(commission = 0.0006)

    # 每次投入資金百份比
    cerebro.addsizer(bt.sizers.PercentSizer, percents = 90)


    
    # 開始回測
    result = cerebro.run()

    
    # 把結果制作成圖表
    print ('夏普比率: ', result[0].analyzers.SharpeRatio.get_analysis()['sharperatio'])
    print ('最大跌幅: ', result[0].analyzers.DrawDown.get_analysis()['max']['drawdown'])

    cerebro.plot()