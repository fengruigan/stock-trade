"""
This is the main python script
Handles api connection and main functions here
"""
import numpy as np
import alpaca_trade_api as tradeapi
from Lib.Modules import indicators
from Lib.Modules import execution as exe
from Lib.Modules.run import keys, context, data
# from Lib.Strategies.strategies import initialize, handle_data
from Lib.Strategies.test import initialize, handle_data, rebalance
import time


# use this method to update user API keys
keys.set_keys(keys, 'PKHDD32BIDCMMLAN59WI', 'U50Ch0jCc/UcTj98rC0OGjSAMMyfwCJ/pvoZW5ts')
exe.init_keys()

# keys.update_key(keys, 'PKHDD32BIDCMMLAN59WI')
# keys.update_secret_key(keys, 'U50Ch0jCc/UcTj98rC0OGjSAMMyfwCJ/pvoZW5ts')
api = tradeapi.REST(keys._key, keys._secret_key, keys._base_url, api_version='v2')

# # running strategy
initialize(context=context)

# need to have a time control for handle_data
run_time = 0
curr_minute = api.get_clock().__getattr__('timestamp').minute
# while (run_time < 1000000):
#     if (api.get_clock().__getattr__('timestamp').minute != curr_minute):
#         curr_minute = api.get_clock().__getattr__('timestamp').minute
#         run_time = run_time + 1
#         print("Strategy ran for " + str(run_time) + " minutes")
#         handle_data(context=context, data=data)
#     else:
#         time.sleep(5)


# print("updated keys should be: " + keys.key)

# rebalance(context=context)
# value = 33333
# print(float(api.get_account().buying_power) > value)
# value = float(api.get_account().portfolio_value) * context.target_position['AAPL']
# print(value)
# print(api.get_last_quote('AAPL').askprice)
#
# pwr = float(api.get_account().buying_power)
# print(pwr > 33333)
# exe.order_value('AAPL', 33333)
# exe.order_percent('AAPL', context.target_position['AAPL'])
# exe.order_target_percent('AAPL', context.target_position['AAPL'])
# print(api.get_account())
