from datetime import datetime
import backtrader as bt

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        # 內建的指標, 如有需要可以自己去官網看, 修改
        sma = bt.ind.SMA(period = 50)
        price = self.data
        crossover = bt.ind.CrossOver(price, sma)
        self.signal_add(bt.SIGNAL_LONG, crossover)
    
    