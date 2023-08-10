from data_fetcher import fetch_data
from strategies import StatArbStrategy
import backtrader as bt
import backtrader.feeds as btfeeds
import logging
import pandas as pd
logging.basicConfig(level=logging.DEBUG)

def run_backtest():
    cerebro = bt.Cerebro()  # Initialize cerebro
    # Fetch data
    data1, data2 = fetch_data('AAPL', 'MSFT')
    print('Stock1 Length: ', data1.size)
    print('Stock2 Length: ', data2.size)

    # Convert pandas Series to backtrader data feeds
    data1_feed = btfeeds.PandasData(dataname=data1)
    data2_feed = btfeeds.PandasData(dataname=data2)

    data1_feed.fromdate = data1.index.min()
    data1_feed.todate = data1.index.max()

    data2_feed.fromdate = data2.index.min()
    data2_feed.todate = data2.index.max()

    cerebro.adddata(data1_feed, name='AAPL')
    cerebro.adddata(data2_feed, name='MSFT')

    # Add strategy to cerebro
    cerebro.addstrategy(StatArbStrategy)

    # Set broker parameters
    cerebro.broker.setcommission(commission=0.001)
    cerebro.broker.set_cash(100000)
    
    # Print out starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    for data in cerebro.datas:
        print('Data Feed Name:', data._name)
        print('Data Feed Length:', len(data))

    # Run cerebro
    cerebro.run()
    
    # Print out final conditions
    print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())


if __name__ == "__main__":
    run_backtest()