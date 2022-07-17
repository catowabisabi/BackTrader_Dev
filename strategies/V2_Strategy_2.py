import backtrader as bt
import datetime

class V2_Strategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, 20)
        self.sma_20 = bt.talib.SMA(self.data, 20)
        self.sma_50 = bt.talib.SMA(self.data, 50)
        
    def next(self):
        buy_sig = (self.data.close > self.sma_20 and self.sma_20 > self.sma_50 ) or self.rsi < 30
        short_sig = (self.data.close < self.sma_20 and self.sma_20 < self.sma_50 ) or self.rsi > 80
        if buy_sig:
            self.buy(size=1)
        elif short_sig:
            self.close()
        
