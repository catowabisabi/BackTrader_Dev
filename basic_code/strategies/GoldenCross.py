import backtrader as bt
import math


# 設定回測所使用的策略
class GoldenCross(bt.Strategy):
    
    params = (('fast', 5), ('slow', 20), ('order_percentage', 0.95), ('ticker', 'AAPL'))

    def __init__(self):
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close, period = self.params.fast, plotname = '5 days moving average'
        )
    
        self.slow_moving_average = bt.indicators.SMA(
            self.data.close, period = self.params.slow, plotname = '20 days moving average'
        )

        self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)
    
    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)

                print('買入 {} 手  {}, 每手股價為: {} USD'.format(self.size, self.params.ticker, self.data.close[0]))

                self.buy(size = self.size)
            
        if self.position.size > 0:
            if self.crossover < 0:
                print('賣出 {} 手  {}, 每手股價為: {} USD'.format(self.size, self.params.ticker, self.data.close[0]))

                self.buy(size = self.size)

