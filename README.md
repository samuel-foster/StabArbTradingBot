StatArbTrading
Statistical Arbitrage Trading strategy implementation using backtrader library.

Description
This project aims to run a backtest for a pair trading strategy, specifically focused on two stocks: AAPL and MSFT. The strategy is based on the principle of mean reversion and uses z-scores to determine entry and exit points.

Getting Started
Prerequisites
Python 3.x
Libraries: backtrader, pandas, numpy, sklearn
Installation
Clone this repository:
bash
Copy code
git clone <repository-url>
Navigate to the project directory:
bash
Copy code
cd StatArbTrading
Install required packages:
Copy code
pip install -r requirements.txt
Usage
To run the backtest:

css
Copy code
python main.py
This will fetch data for AAPL and MSFT, execute the strategy, and print the starting and ending portfolio values.

Strategy Details
The core idea is to check if the price difference (spread) between AAPL and MSFT deviates significantly from its historical mean. The z-score is used to measure this deviation.

If the z-score is above a threshold, it indicates that AAPL is overpriced relative to MSFT. Hence, AAPL is sold, and MSFT is bought.

If the z-score is below a negative threshold, it indicates that MSFT is overpriced relative to AAPL. Hence, MSFT is sold, and AAPL is bought.

If the z-score is between the two thresholds, any open positions are closed.

Important Note
API keys or any sensitive information have been omitted from this repository for security reasons. If you're setting this up, make sure to use your own API keys and not expose them in your version control system.

Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

Feel free to modify the content as you see fit. The above is a starting point for you to build upon.
