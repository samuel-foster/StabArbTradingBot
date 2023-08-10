import backtrader as bt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class StatArbStrategy(bt.Strategy):
    params = (
        ('stock1_index', 0),
        ('stock2_index', 1),
        ('period', 100),
        ('zscore_high', 1.5),
        ('zscore_low', -1.5)
    )

    def __init__(self):
        self.stock1 = self.datas[self.params.stock1_index]
        self.stock2 = self.datas[self.params.stock2_index]

    def next(self):
        date = self.datas[0].datetime.date(0)
        aapl_close = self.datas[0].close[0]
        msft_close = self.datas[1].close[0]

        print(f"Date: {date}, AAPL Close: {aapl_close}, MSFT Close: {msft_close}")

        if len(self.stock1) < self.params.period:
            return

        stock1_closes = [self.stock1.close[i] for i in range(-self.params.period, 0)]
        stock2_closes = [self.stock2.close[i] for i in range(-self.params.period, 0)]

        """For each next() iteration (each time tick), it uses the past period (default 100) closes of the stocks to train a linear regression model. 
            This model predicts stock2's price from stock1's price."""
        model = LinearRegression()
        model.fit(pd.DataFrame(stock1_closes), stock2_closes)

        predicted_stock2 = model.predict(pd.DataFrame([self.stock1.close[-1]]))
        
        """Calculates the current "spread" by taking the difference between the actual close of stock2 and its predicted close (from the linear regression model)."""
        spread = self.stock2.close[0] - predicted_stock2[0]

        mean_spread = np.mean([stock2 - stock1 for stock2, stock1 in zip(stock2_closes, stock1_closes)])
        std_spread = np.std([stock2 - stock1 for stock2, stock1 in zip(stock2_closes, stock1_closes)])

        """The Z-Score is calculated based on the mean and standard deviation of the spread for the past period."""
        zscore_value = (spread - mean_spread) / std_spread

        print(f"Date: {self.data.datetime.date(0)}, Z-Score: {zscore_value}")

        # Check if there are any open positions
        has_position_stock1 = self.getposition(self.stock1).size
        has_position_stock2 = self.getposition(self.stock2).size

        """Trading Signals:
            If the Z-Score is less than zscore_low (default -1.5) and there are no open positions: Buy stock2 and Short stock1.
            If the Z-Score is more than zscore_high (default 1.5) and there are no open positions: Short stock2 and Buy stock1.
            If the Z-Score comes back within the zscore_low and zscore_high range: Close any open positions."""

        if zscore_value < self.params.zscore_low and not has_position_stock1 and not has_position_stock2:
            print(f"Buying Stock2 and Selling Stock1 on Date: {self.stock1.datetime.date(0)}")
            self.buy(data=self.stock2)
            self.sell(data=self.stock1)

        elif zscore_value > self.params.zscore_high and not has_position_stock1 and not has_position_stock2:
            print(f"Selling Stock2 and Buying Stock1 on Date: {self.stock1.datetime.date(0)}")
            self.sell(data=self.stock2)
            self.buy(data=self.stock1)

        elif zscore_value > self.params.zscore_low and zscore_value < self.params.zscore_high:
            print(f"Closing positions on Date: {self.stock1.datetime.date(0)}")
            if has_position_stock1 != 0:
                self.close(data=self.stock1)
            if has_position_stock2 != 0:
                self.close(data=self.stock2)
