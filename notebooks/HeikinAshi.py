
import backtrader as bt
import yfinance as yf
import pandas as pd

cerebro = bt.Cerebro()
df = yf.download("TSLA", start = "2022-01-01")
feed = bt.feeds.PandasData(dataname = df)
#feed.addfilter(bt.filters.HeikinAshi(feed))


cerebro.adddata(feed)
cerebro.run()
cerebro.plot(style='candlestick')