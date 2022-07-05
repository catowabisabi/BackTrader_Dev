import backtrader as bt


# 設定回測所使用的策略
class BuyHold(bt.Strategy):
   
   def next(self):
    if self.position.size == 0 :
        size = int(self.broker.getcash() / self.data)
        self.buy(size = size)