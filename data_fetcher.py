import alpaca_trade_api as tradeapi
import pandas as pd
from alpaca_trade_api import TimeFrame
from secrets_1 import API_KEY, API_SECRET


# Alpaca setup
#API_KEY = 'your_api_key_here'
#API_SECRET = 'your_secret_key_here'
BASE_URL = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(API_KEY, API_SECRET, base_url=BASE_URL)

def fetch_data(stock1_symbol, stock2_symbol, length=300):
    stock1_series = api.get_bars(stock1_symbol, TimeFrame.Day, start="2023-01-01").df['close']
    stock2_series = api.get_bars(stock2_symbol, TimeFrame.Day, start="2023-01-01").df['close']

    # Convert series to DataFrame with column name 'close'
    stock1_data = stock1_series.to_frame(name='close')
    stock2_data = stock2_series.to_frame(name='close')
    
    # Reset the index and rename the old index (which contains dates) to 'datetime'
    stock1_data = stock1_data.reset_index().rename(columns={'timestamp': 'datetime'})
    stock2_data = stock2_data.reset_index().rename(columns={'timestamp': 'datetime'})

    # Convert 'datetime' column to datetime format and set it as index
    stock1_data['datetime'] = pd.to_datetime(stock1_data['datetime']).dt.tz_localize(None)
    stock1_data.set_index('datetime', inplace=True)

    stock2_data['datetime'] = pd.to_datetime(stock2_data['datetime']).dt.tz_localize(None)
    stock2_data.set_index('datetime', inplace=True)
    
    return stock1_data, stock2_data

