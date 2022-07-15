import backtrader as bt

class TrendBand(bt.Strategy):
    
    lines = ('mid','top','bot',)
    params = (('maperiod',20),
              ('period',3),
              ('highRate',1.2),
              ('lowRate',0.85),)
              
    # 與價格在同一張圖內顯示
    plotinfo = dict(subplot=False)

    def __init__(self):
        
        ema = bt.ind.EMA(self.data, period=self.p.maperiod)
        
        # 上中下試的計算
        self.l.mid=bt.ind.EMA(ema,period=self.p.period)

        self.l.top=bt.ind.EMA(self.mid*self.p.highRate,\
                              period=self.p.period)

        self.l.bot=bt.ind.EMA(self.mid*self.p.lowRate,\
                              period=self.p.period)
        super(TrendBand, self).__init__()

class TestStrategy2(bt.Strategy):

    def __init__(self):
        
        TrendBand(self.data)


class TrendBand_Strategy(bt.Strategy):

    params=(('period',20),)

    def __init__(self):
        pass
        self.order = None
        self.mid = TrendBand(self.data).mid 
        self.top = TrendBand(self.data).top
        self.bot = TrendBand(self.data).bot

        # 設罝買入訊號, 三者同時符合
        self.buy_sig=bt.And(\
           self.data.close>self.mid,\
           self.data.volume==bt.ind.Highest(\
           self.data.volume,period=self.p.period))

        # 設置賣出訊號
        self.sell_sig=self.data.close>self.top
        

    def next(self):
        pass
        if not self.position:
            # 現時戶口內有多少錢
            total_value = self.broker.getvalue()

            #1手=100股，全買
            ss=int((total_value/100)/self.datas[0].close[0])*100
            if self.buy_sig:
                self.order=self.buy(size=ss)
        else:
            if self.sell_sig:
                self.close()