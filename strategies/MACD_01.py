import backtrader as bt

class MACD_01(bt.Strategy):

    def __init__(self):
        bt.ind.MACD(self.data)
        bt.ind.MACDHisto(self.data)
        bt.ind.RSI(self.data,period=14)
        bt.ind.BBands(self.data)

class MACD_02(bt.Strategy):

    params=(('p1',12),('p2',26),('p3',9),)
    def __init__(self):
        self.order = None

        # 建立 macd 柱狀圖 的物件
        self.macdhist = bt.ind.MACDHisto(self.data,
                        period_me1=self.p.p1, 
                        period_me2=self.p.p2, 
                        period_signal=self.p.p3)

    def next(self):
        if not self.position:

            # 拿現時戶口內有的錢
            total_value = self.broker.getvalue()

            # 1手=100股，所有錢全買
            ss=int((total_value/100)/self.datas[0].close[0])*100

            # 當MACD柱大於0（紅柱）且無持倉時滿倉買入
            if self.macdhist > 0:
                self.order=self.buy(size=ss)
        else:
            # 當MACD柱小於0（綠柱）滿倉賣出
            if self.macdhist < 0:
                self.close()