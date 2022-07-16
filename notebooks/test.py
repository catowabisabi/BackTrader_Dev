import yfinance as yf
import pandas as pd
import backtrader as bt
import pandas_ta as ta

pd.set_option('display.max_rows', None)
df = yf.download("TSLA", start = "2020-01-01")
df = df.sort_values(by="Date", ascending=False)
df.ta.supertrend(period=7, multiplier=3, append=True)

print(df)

feed = bt.feeds.PandasData(dataname = df)

df1 = pd.DataFrame()

df1['open'] = df["Open"]
df
print(df1)

