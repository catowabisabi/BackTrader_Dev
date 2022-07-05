from calendar import c
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as py

back_test_stock_csv = 'AAPL'
stock_data_path = '..\\stock_price_csv\\{}.csv'.format(back_test_stock_csv)


csv_path = stock_data_path




# 設定回測所使用的策略
class SMA_Strategy(bt.Strategy):
    def __init__(self):
        #定義每支K線的收巿價為data0 內的close, 如果有多過一組的data, 需要把0改為其他的數字
        self.dataclose = self.data0.close
        
        # 這些是基本設定, 照打就OK
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # ============================ 技術指標設定 ===========================
        self.sma = bt.indicators.SimpleMovingAverage(self.data0, period = 15)

    # ============================ 設定每支K線後的策略 =========================
    def next(self):
        
        # (1) 如果沒有持有倉位
        if not self.position:
            # 如果當日的收巿價 大於(升穿) sma (以上設定的15日線) (其實只要高過就買, 
            # 係無升穿呢個羅輯, 如果要寫呢個羅輯, 要計算係dataclose[-1] 前一日收巿係咪低於sma[-1] 前一日既sma
            # 但我個人認為呢個羅輯意思意不太大, 而呢個只係一個好簡單既低能策略, 所以唔使搞得咁覆雜。)
            if self.dataclose[0] > self.sma[0]:
                # 買入
                self.buy()
        
        # (2) 如果手中持有倉位
        else:
            # 如果當日K線收巿價 低於(跌穿) sma (以上設定的15日線)
            if self.dataclose[0] < self.sma[0]:
                # 把手中持有的倉位賣出
                self.close()
                # 做空
                self.sell()

#============================================== 資料notification ======================

    # notification
    def notify_order(self, order):
        
        # 如果訂單的情況是 "己提交" 或 "己接收", 什麼都不做
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 如果訂單的情況是 "己完成"
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    '買入訂單完成! 價格為:{} 成本為:{} 佣金為:{}'
                    .format(
                        order.executed.price, 
                        order.executed.value, 
                        order.executed.comm, )
                        )

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(
                    '賣出訂單完成! 價格為:{} 成本為:{} 佣金為:{}'
                    .format(
                        order.executed.price, 
                        order.executed.value, 
                        order.executed.comm, )
                        )
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('訂單已 取消/Margin/被拒')
        self.order = None
    
    
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION 回報, Gross {}, Net {}'.format(trade.pnl, trade.pnlcomm))

    def log(self, txt, dt = None, doprint = True):
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print ('%s, %s' %(dt.isoformat(), txt))

#============================================== 資料notification ======================

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
    cerebro.addstrategy(SMA_Strategy)

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