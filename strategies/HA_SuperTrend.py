import backtrader as bt
from backtrader.indicators import SuperTrend
from strategies.my_indicators.SuperTrend import SuperTrend
import pandas_ta as ta


class HA_SuperTrend(bt.Strategy):

# 策略初始化
# 策略內容
    # 計算指標
    # 買賣Logic
    # TP/SL 計算 (分批SL)

# 顯示記綠
# 自定功能

#=====================策略初始化 開始==================================

    # 呢個要改 - 只係行一次
    def __init__(self):
        
        # 拿取 OHLCV
        self.datadate   = self.datas[0].datetime
        self.dataclose  = self.datas[0].close
        self.dataopen   = self.datas[0].open
        self.datahigh   = self.datas[0].high
        self.datalow    = self.datas[0].low
        self.datavolume = self.datas[0].volume

        # SuperTrend
        

        self.super_trend_ind = ta.supertrend(self.datahigh, self.datalow, self.dataclose, 10, 3)
       


        
        
        # 初始化 
        self.order      = None # 
        self.buyprice   = None # 股價
        self.buycomm    = None # 佣金

#=====================策略初始化 完結==================================



#=====================策略內容 開始==================================


    # 每一支K線開始就會行一次呢行野
    def next(self):
        
        # 最新對上1支K線的收巿價
        #self.log('K線收巿價, %.2f' % self.dataclose[0])
        sti = ta.supertrend(self.datahigh, self.datalow, self.dataclose, 10, 3)
        print(sti)

        

        
        
        

    #=====================計算指標 開始==================================

        # 計算 現在的True Range
        self.true_range = tr(   previous_close  = self.dataclose[-1],   \
                                high            = self.datahigh[0],     \
                                low             = self.datalow[0]           )
        
        # 計算 ATR
        self.atr = bt.indicators.ATR(self.data, period=10)

        # 計算 SuperTrend
        self.st = SuperTrend(period = 7, multiplier = 3)
        
    #=====================計算指標 完結==================================
        

        # 如果本身有order係落緊未完成交易, 就唔買
        if self.order:
            return

        
        # 如果我地本身無野買左係手
        if not self.position:
            return

            # 呢個策略係連升兩日, 今日高過琴日, 琴日又高過前日
            if self.dataclose[0] < self.dataclose[-1]:
                    if self.dataclose[-1] < self.dataclose[-2]:

                        self.log('發出買入訂單, %.2f' % self.dataclose[0])
                        self.order = self.buy()

        else: # 如果有野係手
            return

            # 如果拎住左5枝K就賣    #買個支K線
            if len(self) >= (self.bar_executed + 5):
        
                self.log('發出賣出訂單, %.2f' % self.dataclose[0])
                self.order = self.sell()

#=====================策略內容 完結==================================



#=====================顯示記綠 開始==================================
#=====================顯示記綠 開始==================================
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
                    '已執行買入訂單, 價格: %.2f, 成本: %.2f, 佣金 %.2f \n' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm

            # 如果你;賣貨
            else:  # Sell
                self.log('已執行賣出訂單, 價格: %.2f, 成本: %.2f, 佣金 %.2f \n\n' %
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

#=====================顯示記綠 完結==================================
#=====================顯示記綠 完結==================================



#=====================自定功能 開始==================================

# 計算True Range
def tr(previous_close, high, low):
    price_diff_1 = abs(high - low)
    price_diff_2 = abs(high - previous_close)
    price_diff_3 = abs(low - previous_close)

    tr = max (price_diff_1, price_diff_2, price_diff_3)
    return tr

def atr(data, period):
    data['tr'] = tr(data)
    atr = data['tr'].rolling(period).mean()

    return atr

def supertrend(df, period=7, atr_multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    df['atr'] = atr(df, period)
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True

        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False

        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]
        
    return df

#=====================自定功能 完結==================================

#=====================     完     ==================================

    