"""
This is the main script for backtesting
"""
from Lib.Backtest.run import API, keys, Data, Context, Clock
from Lib.Backtest.account import Account
from Lib.Backtest.Strategies.test import initialize, handle_data
import matplotlib.pyplot as plt
import pandas as pd
import time


keys.set_keys(keys, 'PKFE10XOBD7S4S5PYW4S', 'OQaJy/hcLjrNSNubTbUTpqbH21ybe/Dow65YYBfu')
API.init_api(API)

initialize(Context)
start = pd.Timestamp('2019-01-01', tz='America/New_York').isoformat()
# end2 = pd.Timestamp('2019-01-03', tz='America/New_York')
end = pd.Timestamp('2020-01-01', tz='America/New_York').isoformat()
minute_delta = str(Context.params['trade_freq']) + ' minute'
Clock.init_clock(Clock, Context, start=start, end=end, minute_delta=minute_delta)
Account.init_account(Account, capital=100000)
t0 = time.time()
while (Clock.is_running):
    handle_data(Context, Data)

t1 = time.time() - t0
print("runtime is " + str(t1))

print(Account.get_account(Account))
plt.plot(Clock.dateline, Account.portfolio_history)
plt.show()

