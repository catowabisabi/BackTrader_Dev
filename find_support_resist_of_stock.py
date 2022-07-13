import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import mplfinance as mpf

yf.pdr_override() # activate yahoo finance workaround

timeD = dt.timedelta(days = 60) #線的長度
now = dt.datetime.now()
start = now - timeD

stock = input("\n請輸入股票symbol (輸入'quit'退出): ")




while stock != "quit" and stock != "Quit":

    df = pdr.get_data_yahoo(stock, start, now)
    df["High"].plot(label = "high")
#===========================================
    




#===============================================================

    pivots = []
    dates = []
    counter = 0
    lastPivot = 0
    
    Range = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dateRange = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in df.index:
        currentMax = max (Range, default=0)
        value = round(df["High"][i], 2)

        Range = Range[1:9]
        Range.append(value)

        dateRange = dateRange[1:9]
        dateRange.append(i)

        if currentMax == max (Range, default=0):
            counter += 1
        else:
            counter = 0

        if counter  == 5:
            lastPivot = currentMax
            dateloc = Range.index(lastPivot)
            lastDate = dateRange[dateloc]

            pivots.append(lastPivot)
            dates.append(lastDate)
    print()
    #print(str(Range))
    #print(str(dateRange))

    #print (str(pivots))
    #print (str(dates))

    timeD = dt.timedelta(days = 30) #線的長度

    for index in range(len(pivots)):
       # print(str(pivots[index]) +" : " + str(dates[index]))

        plt.plot_date([dates[index], dates[index]+timeD], [pivots[index], pivots[index]], linestyle = "-", linewidth = 2, marker = ",", color = 'green')
    

#=======================================================================


    df["Low"].plot(label = "low", color = "red")

    pivots_low = []
    dates_low = []
    counter_low = 0
    lastPivot_low = 9999
    
    Range_low = [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999]
    dateRange_low = [9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999, 9999]

    for i in df.index:
        currentMin = min (Range_low, default=0)
        value_low = round(df["Low"][i], 2)

        Range_low = Range_low[1:9]
        Range_low.append(value_low)

        dateRange_low = dateRange_low[1:9]
        dateRange_low.append(i)

        if currentMin == min (Range_low, default=0):
            counter_low += 1
        else:
            counter_low = 0

        if counter_low  == 5:
            lastPivot_low = currentMin
            dateloc_low = Range_low.index(lastPivot_low)
            lastDate_low = dateRange_low[dateloc_low]

            pivots_low.append(lastPivot_low)
            dates_low.append(lastDate_low)
    print()
   # print(str(Range_low))
   # print(str(dateRange_low))

    #print (str(pivots))
    #print (str(dates))

    timeD = dt.timedelta(days = 30) #線的長度

    for index in range(len(pivots_low)):
        #print(str(pivots_low[index]) +" : " + str(dates_low[index]))
       

        plt.plot_date([dates_low[index], dates_low[index]+timeD], [pivots_low[index], pivots_low[index]], linestyle = "-", linewidth = 2, marker = ",", color = 'red')






#=====================================================================


    plt.show()
    stock = input("\n請輸入股票symbol (輸入'quit'退出): ")
