"""
This is the main script for backtesting
"""
from Lib.Backtest.run import API, keys, Data, Context, Clock
from Lib.Backtest.account import Account
from Lib.Backtest.Strategies.test import initialize, handle_data
import matplotlib.pyplot as plt


keys.set_keys(keys, 'PKFE10XOBD7S4S5PYW4S', 'OQaJy/hcLjrNSNubTbUTpqbH21ybe/Dow65YYBfu')
API.init_api(API)

initialize(Context)
start = '2019-01-02'
end = '2019-01-05'
Clock.init_clock(Clock, start=start, end=end, minute_delta=str(Context.params['trade_freq']) + ' minute')
Account.init_account(Account, capital=100000)
while (Clock.is_running):
    handle_data(Context, Data)

# print(Account.get_account(Account))
plt.plot(Clock.timeline, Account.portfolio_history)
plt.show()


