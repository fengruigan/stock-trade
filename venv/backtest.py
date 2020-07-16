"""
This is the main script for backtesting
"""
import pandas as pd
from Lib.Backtest.run import API, keys, data, context, Clock
from Lib.Backtest.account import Account
from Lib.Backtest.Strategies.test import initialize, handle_data


keys.set_keys(keys, 'PKFE10XOBD7S4S5PYW4S', 'OQaJy/hcLjrNSNubTbUTpqbH21ybe/Dow65YYBfu')
API.init_api(API)
Clock.init_clock(Clock, start='2019-01-01', end='2020-01-01')
