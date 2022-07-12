import backtrader as bt
import yfinance as yf
from stock_config import *
from strategies import BuyHold





if __name__ == '__main__':
    # 一切由這裏開始
    # 請到stock_config修改相關數值

    cerebro = bt.Cerebro()
    try:
        df = yf.download(my_stock, start = my_backtest_start_day) #stock_config BackTest日期 股票
        #print (df)

    except Exception as e:
        print(e)

    feed = bt.feeds.PandasData(dataname = df)
    cerebro.adddata(feed)

    #============加載策略 (請使用 strategies 文件夾內的 Template)==========
    cerebro.addstrategy(BuyHold.BuyHold)

    #============加載佣金, 下注金額, 分析器================================
    cerebro.broker.setcommission(commission=my_broker_commission) #stock_config 佣金

    cerebro.addsizer(bt.sizers.PercentSizer, percents = my_PercentSizer) #stock_config 下注金額

    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='ta')
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', riskfreerate=0.0, annualize=True, timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(bt.analyzers.VWR, _name='vwr')
    cerebro.addanalyzer(bt.analyzers.SQN, _name='sqn')
    cerebro.addanalyzer(bt.analyzers.Transactions, _name='txn')

    # cerebro.addanalyzer(bt.analyzers.DrawDown, _name = "drawdown")
    # cerebro.addanalyzer(bt.analyzers.Returns, _name = "returns")
    # cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name = "my_annual_return") # 2 vars
    # cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')

    # 開始的資金是多少
    cerebro.broker.setcash(initial_capital)

    #============加載分析器=================================================???
    #cerebro.addobserver(bt.observers.Broker)
    cerebro.addobserver(bt.observers.BuySell)
    cerebro.addobserver(bt.observers.Value)
    cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addobserver(bt.observers.Trades)



    #===========分析器結果 輸出===========================================
    # sharpe_ratio = analyzer_result.analyzers.mysharpe.get_analysis() # 名字要和上邊的 _name 一致
    # annual_return = analyzer_result.analyzers.my_annual_return.get_analysis()  # 名字要和上邊的 _name 一致
    # returns = analyzer_result.analyzers.returns.get_analysis()  # 名字要和上邊的 _name 一致
    # drawdown = analyzer_result.analyzers.drawdown.get_analysis()  # 名字要和上邊的 _name 一致

    # print(sharpe_ratio)
    # print(annual_return)
    # print(returns)
    # print(drawdown)

    # 資料有無係度, 如果有就True
    def exists(object, *properties):
        for property in properties:
            if not property in object: return False
            object = object.get(property)
        return True

    def pretty_print(format, *args):
        print(format.format(*args))



    def printTradeAnalysis (cerebro, analyzers):
        print('\n BUY and Hold 結果')
        format = "        {:<38}:{:<18} {:<28}"
        NA     = '-'

        if hasattr(analyzers, 'ta'):
            ta = analyzers.ta.get_analysis()

            openTotal         = ta.total.open          if exists(ta, 'total', 'open'  ) else None
            closedTotal       = ta.total.closed        if exists(ta, 'total', 'closed') else None
            wonTotal          = ta.won.total           if exists(ta, 'won',   'total' ) else None
            lostTotal         = ta.lost.total          if exists(ta, 'lost',  'total' ) else None

            streakWonLongest  = ta.streak.won.longest  if exists(ta, 'streak', 'won',  'longest') else None
            streakLostLongest = ta.streak.lost.longest if exists(ta, 'streak', 'lost', 'longest') else None

            pnlNetTotal       = ta.pnl.net.total       if exists(ta, 'pnl', 'net', 'total'  ) else None
            pnlNetAverage     = ta.pnl.net.average     if exists(ta, 'pnl', 'net', 'average') else None

            # pretty_print(format, 'Open Positions', openTotal   or NA, '')
            # pretty_print(format, 'Closed Trades',  closedTotal or NA, '所有已平倉交易' )
            # pretty_print(format, 'Winning Trades', wonTotal    or NA, '獲利交易次數')
            # pretty_print(format, 'Loosing Trades', lostTotal   or NA, '虧損交易次數')
            # print('\n')

            # pretty_print(format, 'Longest Winning Streak',   streakWonLongest  or NA, '最大連續獲利交易次數' )
            # pretty_print(format, 'Longest Loosing Streak',   streakLostLongest or NA, '最大連續虧損交易次數')
            # pretty_print(format, 'Strike Rate (Win/closed)', round(((wonTotal / closedTotal) * 100), 2) if wonTotal and closedTotal else NA, '勝率')
            # print('\n')

            pretty_print(format, 'Inital Portfolio Value','${}'.format(initial_capital), '開始本金' )
            pretty_print(format, 'Final Portfolio Value','${}'.format(round(cerebro.broker.getvalue(), 2)), '最終戶口價值' )
            pretty_print(format, 'Final Value / Inital Value', '{}%'.format(round(((cerebro.broker.getvalue()-initial_capital)/initial_capital)*100,2))  or NA, '戶口價值增長%')
            print('\n\n\n')
            # pretty_print(format, 'Net P/L','${}'.format(round(pnlNetTotal,   2)) if pnlNetTotal   else NA, '淨利')
            # pretty_print(format, 'P/L Average per trade','${}'.format(round(pnlNetAverage, 2)) if pnlNetAverage else NA, '平均獲利交易')
            # print('\n')

        # if hasattr(analyzers, 'drawdown'):
        #     pretty_print(format, 'Drawdown', '${}'.format(round(analyzers.drawdown.get_analysis()['max']['drawdown'], 2)), '最大可能虧損' )
        # if hasattr(analyzers, 'sharpe'):
        #     pretty_print(format, 'Sharpe Ratio', round(analyzers.sharpe.get_analysis()['sharperatio'], 2), '夏普比率' )
        # if hasattr(analyzers, 'vwr'):
        #     pretty_print(format, 'VWR', round(analyzers.vwr.get_analysis()['vwr'], 2), '可變性加權回報' )
        # if hasattr(analyzers, 'sqn'):
        #     pretty_print(format, 'SQN', round(analyzers.sqn.get_analysis()['sqn'],2), '系統品質指標' )
        # print('\n')

        # print('交易記錄')
        # print (str(analyzers))
        # format = "  {:<28} {:<18} {:<18} {:<8} {:<8} {:<18} "
        # pretty_print(format, 'Date', 'Stock Amount', 'Stock Price', 'SID', 'Symbol', 'Account Value')
        # for key, value in analyzers.txn.get_analysis().items():
        #     pretty_print(format, key.strftime("%Y/%m/%d %H:%M:%S"), round(value[0][0],2), round(value[0][1],2), value[0][2], value[0][3], round(value[0][4],2))


    # print (annual_return)
    # par_list = [[
    #             returns['rnorm100'],
    #             drawdown['max']['drawdown'],
    #             sharpe_ratio['sharperatio'],


    #             ] for x in analyzer_results]

    # par_df = pd.DataFrame(par_list, columns = ['回報', '最大虧損', '夏普比率'])
    # print('\n\n')
    # print (par_df)
    # print('\n\n')
    # Print some analytics

    #============運行結果 輸出============================================
    analyzer_results = cerebro.run()
    analyzer_result = analyzer_results[0] #分析器結果在[0]

    #===========圖表制作=================================================

    printTradeAnalysis(cerebro, analyzer_result.analyzers)

    # Finally plot the end results
    #cerebro.plot(style='candlestick', volume=False)

