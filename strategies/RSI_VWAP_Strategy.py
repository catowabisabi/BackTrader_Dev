import backtrader as bt
import talib as ta



#=====================指標初始化 開始==================================

class RSI_VWAP(bt.Indicator):

    # 一開始需要用既parameters會係度呢定義
    lines = ('rsi_vwap',)
    params = dict(
        period=14,  # to apply to RSI
        pperiod=None,  # if passed apply to HighestN/LowestN, else "period"
    )

    def __init__(self):
        rsi = bt.talib.RSI(self.data, timeperiod=self.p.period)

        pperiod = self.p.pperiod or self.p.period
        maxrsi = bt.ind.Highest(rsi, period=pperiod)
        minrsi = bt.ind.Lowest(rsi, period=pperiod)

        self.l.stochrsi = (rsi - minrsi) / (maxrsi - minrsi)
        
#=====================指標初始化 完結==================================



class StochRSIStrategy(bt.Strategy):

#=====================策略初始化 開始==================================

    # 一開波做一次, 好似係, 除非唔係
    def __init__(self):

        # 導入指標
        self.stochrsi_indicator = StochRSI()

        # 有無買緊野
        self.order_exist = False

        self.dataclose = self.data0.close
        self.order = None
        self.buyprice = None
        self.buycomm = None

#=====================策略初始化 完結==================================

    # 買賣的定義
    def next(self):
        previous_stochrsi = self.stochrsi_indicator.lines.stochrsi[-1]
        current_stochrsi = self.stochrsi_indicator.lines.stochrsi[0]
        buy_signal = previous_stochrsi < current_stochrsi and current_stochrsi < 0.2
        sell_signal = previous_stochrsi > current_stochrsi and current_stochrsi > 0.8 # 只係定義signal

        if self.order:
            return


        if buy_signal and not self.position:
            print (buy_signal)
            print (f'買買買: {current_stochrsi}')

            # BUY, BUY, BUY!!! (with default parameters)
            self.log('發出買入訂單, %.2f' % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.order = self.buy()
            #self.buy()
            #self.ordr_exist = True
        
        if sell_signal and self.position:
            print (f'賣賣賣: {current_stochrsi}')

            # SELL, SELL, SELL!!! (with all possible default parameters)
            self.log('發出賣出訂單, %.2f' % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.order = self.sell()

            #self.sell()
            #self.order_exist = False






#========================== 照抄就OK ==========================
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
