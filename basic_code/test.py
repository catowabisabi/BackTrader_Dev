from AlgorithmImports import *

from tensorflow.keras.models import Sequential
import json
# endregion

class AdaptableFluorescentOrangeAlligator(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2017, 12, 28)  # Set Start Date
        self.SetEndDate (2020,1,1)

        model_key = model_key = 'bitcoin_price_predictor'
        # 如果qb store入邊有model_key, 就拎佢出黎用
        if self.ObjectStore.ContainsKey(model_key):
            model_str = self.ObjectStore.Read(model_key)
            #變成json
            config = json.loads(model_str)['config']
            #再變成要用既class
            self.model = Sequential.from_config(config)

        
        self.SetBrokerageModel(BrokerageName.Bitfinex, AccountType.Margin)
        self.SetCash(10000)  # Set Strategy Cash
        self.symbol = self.AddCrypto("BTCUSD", Resolution.Daily).Symbol
        self.SetBenchmark(self.symbol)
        #self.AddEquity("SPY", Resolution.Minute)
        #self.AddEquity("BND", Resolution.Minute)
        #self.AddEquity("AAPL", Resolution.Minute)

    def OnData(self, data: Slice):
        if self.GetPrediction() == "Up":
            self.SetHoldings(self.symbol, 0.05)
        else: 
            self.SetHoldings(self.symbol, -0.05)

    def GetPrediction(self):
        # 拎最近40日既資料
        df = self.History(self.symbol, 40).loc[self.symbol]
        df_change = df[["open", "high", "low", "close", "volume"]].pct_change().dropna()

        #變成要用既format
        model_input = []

        for index, row in df_change.tail(30).iterrows():
            model_input.append(np.array(row))
        model_input = np.array([model_input])
        if round (self.model.predict(model_input)[0][0]) == 0:
            return "Down"
        else:
            return "Up"