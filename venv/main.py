"""
This is the main python script
Handles api connection and main functions here
"""
import numpy as np
import alpaca_trade_api as tradeapi
from Lib.Modules import indicators
from Lib.Modules import execution
from Lib.Modules.user_config import keys


keys.update_key(keys, 'PKH1K1LTH0541LAZHXMT', 'r/bnsex3KAFlxYgwM0Z0LtS4Vu3IqLsuPqRCEFEt')
api = tradeapi.REST(keys.key, keys.secret_key, keys.base_url, api_version='v2')


# api.submit_order(symbol="AAPL", qty=1, side="buy", type="market", time_in_force="gtc")

# print(execution.order_value("MSFT", 1000))

# price = api.get_last_quote("MSFT")
# print(price)
# cfg = api.get_account()
# print(cfg)
