import backtrader as bt

class StochRSI(bt.Indicator):

    

    # 一開始需要用既parameters會係度呢定義
    lines = ('stochrsi',) #一定要加個  ","
    params = {
        'period' : 14
    }

    def __init__(self):
        period1 = self.params.period

        rsi = bt.indicators.RSI(self.data, period = period1)
        maxrsi = bt.indicators.Highest(rsi, period = period1)
        minrsi = bt.indicators.Lowest(rsi, period = period1)
        self.lines.stockrsi = (rsi - minrsi) / (maxrsi - minrsi)


