import backtrader as bt

class My_Strategies_Common_Funtion:

        # 照抄就OK
    def log(self, txt, dt=None):
        ''' Logging function for this strategy
            這個功能是用作Log唔同既信息'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            # 如果個broker接受左你個order, 交易左啦, 咁呢度就乜都唔使做
            # 如果未交易, 就會check下下邊係邊個status, report返比我地知
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        # 如果你買既時候你個戶口唔夠錢, 就唔會complete, 咁呢度都唔行
        if order.status in [order.Completed]:
            # 如果你買貨
            if order.isbuy():
                self.log(
                    #'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    '已執行買入訂單, 價格: %.2f, 成本: %.2f, 佣金 %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

            # 如果你;賣貨
            else:  # Sell
                self.log('已執行賣出訂單, 價格: %.2f, 成本: %.2f, 佣金 %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            # 呢個係用黎計算長度, 一支K線為之一, 係呢個策略度呢個唔好郁佢
            # 佢用黎計賣出時間, 下邊有講, 另外用黎計最少拎住幾耐
            self.bar_executed = len(self) # <===============注意
#====注意====>

        # 如果訂單出現問題
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('訂單 取消/保証金不足/被拒')
                # 該訂單的執行將意味著追加保証金的需要, 而且, 之前所接受的訂單已從系統中刪除

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('平倉利潤, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))