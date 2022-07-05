import backtrader as bt
import datetime
import yfinance as yf
from stock_config import * 
from strategies import Simple_Strategy_02


# 一切由這裏開始
# 請到stock_config修改相關數值

cerebro = bt.Cerebro()
df = yf.download(my_stock, start = my_backtest_start_day) #stock_config BackTest日期 股票
print (df)
feed = bt.feeds.PandasData(dataname = df)
cerebro.adddata(feed)

#============加載策略 (請使用 strategies 文件夾內的 Template)==========
cerebro.addstrategy(Simple_Strategy_02.TestStrategy)

#============加載佣金, 下注金額, 分析器================================
cerebro.broker.setcommission(commission=my_broker_commission) #stock_config 佣金
cerebro.addsizer(bt.sizers.PercentSizer, percents = 50) #stock_config 下注金額
cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name = "my_annual_return") # 2 vars
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe') 

#============運行結果 輸出============================================
analyzer_results = cerebro.run()
analyzer_result = analyzer_results[0] #分析器結果在[0]

#===========圖表制作=================================================
cerebro.plot()

#===========分析器結果 輸出===========================================
sharpe_ratio = analyzer_result.analyzers.mysharpe.get_analysis() # 名字要和上邊的 _name 一致
annual_return = analyzer_result.analyzers.my_annual_return.get_analysis()  # 名字要和上邊的 _name 一致

print(sharpe_ratio)
print(annual_return)