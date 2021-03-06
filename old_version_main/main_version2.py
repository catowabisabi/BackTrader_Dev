import backtrader as bt
import datetime
import yfinance as yf
from stock_config import * 
from strategies import SMA_Cross
import pandas as pd





if __name__ == '__main__':
    # 一切由這裏開始
    # 請到stock_config修改相關數值

    cerebro = bt.Cerebro()
    try:
        df = yf.download(my_stock, start = my_backtest_start_day) #stock_config BackTest日期 股票
        print (df)

    except Exception as e:
        print(e)

    feed = bt.feeds.PandasData(dataname = df)
    cerebro.adddata(feed)

    #============加載策略 (請使用 strategies 文件夾內的 Template)==========
    cerebro.addstrategy(SMA_Cross.Sma_Cross)

    #============加載佣金, 下注金額, 分析器================================
    cerebro.broker.setcommission(commission=my_broker_commission) #stock_config 佣金
    cerebro.addsizer(bt.sizers.PercentSizer, percents = my_PercentSizer) #stock_config 下注金額
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name = "drawdown")
    cerebro.addanalyzer(bt.analyzers.Returns, _name = "returns")
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
    returns = analyzer_result.analyzers.returns.get_analysis()  # 名字要和上邊的 _name 一致
    drawdown = analyzer_result.analyzers.drawdown.get_analysis()  # 名字要和上邊的 _name 一致

    # print(sharpe_ratio)
    # print(annual_return)
    # print(returns)
    # print(drawdown)

    # 資料有無係度, 如果有就True


    print (annual_return)
    par_list = [[
                returns['rnorm100'], 
                drawdown['max']['drawdown'],
                sharpe_ratio['sharperatio'],
                
                
                ] for x in analyzer_results]

    par_df = pd.DataFrame(par_list, columns = ['回報', '最大虧損', '夏普比率'])
    print('\n\n')
    print (par_df)
    print('\n\n')

