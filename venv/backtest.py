"""
This is the main script for backtesting
"""
from Lib.Backtest.run import API, keys, Data, Context, Clock
from Lib.Backtest.account import Account
import matplotlib.pyplot as plt
import pandas as pd
import time
from Lib.Backtest.Strategies.test import initialize, handle_data
import numpy as np

## parameters to change
alpaca_key = 'PKFE10XOBD7S4S5PYW4S'
alpaca_secret_key = 'OQaJy/hcLjrNSNubTbUTpqbH21ybe/Dow65YYBfu'
start_date = '2019-03-05'
end_date = '2019-03-13'
capital = 100000


######## ignore the rest
keys.set_keys(keys, alpaca_key, alpaca_secret_key)
API.init_api(API)
initialize(Context)
start = pd.Timestamp(start_date, tz='America/New_York').isoformat()
end = pd.Timestamp(end_date, tz='America/New_York').isoformat()
minute_delta = str(Context.params['trade_freq']) + ' minute'
t0 = time.time()
Clock.init_clock(Clock, Context, start=start, end=end, minute_delta=minute_delta)
print("Data collection time: " + str(time.time() - t0) + " seconds")
Account.init_account(Account, capital=capital)
t0 = time.time()
while (Clock.is_running):
    handle_data(Context, Data)

t1 = time.time() - t0
print("runtime is " + str(t1))

print(Account.get_account(Account))
plt.plot(Clock.dateline, Account.portfolio_history)
plt.show()