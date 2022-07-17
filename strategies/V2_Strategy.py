import backtrader as bt
import datetime

class RMI_Condition():
    pass

class RMI(bt.Indicator):
    lines = ('rmi_long', 'rmi_short',)
    
    def __init__(self):
        rmi = bt.ind.RelativeMomentumIndex(period = 26, lookback = 29)
        
        #if bt.ind.CrossOver(rmi, 70):
        #     signal = -1
        # if bt.ind.CrossDown(rmi, 30):
        #     signal = 1
        # else:
        #     signal = 0
        
        #rmi3 = bt.ind.rmi(period = 200)
        self.l.rmi_long = bt.ind.CrossOver(rmi, 70)
        self.l.rmi_short = bt.ind.CrossDown(rmi, 30)

        





class V2_Strategy(bt.SignalStrategy):
    def __init__(self):
        rmi = RMI()

        self.signal_add(bt.SIGNAL_LONG, rmi.l.rmi_long)
        self.signal_add(bt.SIGNAL_SHORT, rmi.l.rmi_short)

