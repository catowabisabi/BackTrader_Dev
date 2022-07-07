import pandas as pd
import pandas_ta as ta
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time

#pd.set_option('display.float_format', lambda x: '%.8f' % x)
df = pd.read_csv("./stock_data/Bitstamp_BTCUSD_d.csv", header = [1])
df = df[["unix", "open", "high", "low", "close", "Volume USD"]]
df["volume"] = df["Volume USD"]
del df["Volume USD"]
df.sort_values(by="unix", inplace = True)
df["date"] = pd.to_datetime(df["unix"], unit = 's')
df.set_index(pd.DatetimeIndex(df["date"]), inplace=True)
df["VWAP"] = ta.vwap (close = df.close, high = df.high, low = df.low, volume= df.volume)
df["RSI_VWAP_20"] = ta.rsi(close = df.VWAP, length = 20)
df["SMA250"] = ta.sma(close=df.close, length = 250)

# plt.plot(df.date, df.SMA250)
# plt.plot(df.date, df.close)
# plt.show()

hadf = ta.ha(
open_ = df.open,
    close = df.close,
    high = df.high,
    low = df.low,

)
#print (df)
#print (hadf)


fig = go.Figure(data = [go.Candlestick(
    x = df.date,
    open = hadf.HA_open,
    close = hadf.HA_close,
    high = hadf.HA_high,
    low = hadf.HA_low,

)])


fig.show()
time.sleep(1)

