"""
This is the main python script
Handles api connection and main functions here
"""
import numpy as np
import alpaca_trade_api as tradeapi
from Lib.Modules import indicators
from Lib.Modules import execution as exe
from Lib.Modules.run import keys, context, data
from Lib.Strategies.strategies import initialize, handle_data
import time


# use this method to update user API keys
keys.update_key(keys, 'PKHDD32BIDCMMLAN59WI', 'U50Ch0jCc/UcTj98rC0OGjSAMMyfwCJ/pvoZW5ts')
api = tradeapi.REST(keys.key, keys.secret_key, keys.base_url, api_version='v2')

# # running strategy
initialize(context=context)

# need to have a time control for handle_data
run_time = 0
curr_minute = api.get_clock().__getattr__('timestamp').minute
while (run_time < 1000000):
    if (api.get_clock().__getattr__('timestamp').minute != curr_minute):
        curr_minute = api.get_clock().__getattr__('timestamp').minute
        run_time = run_time + 1
        print("Strategy ran for " + str(run_time) + " minutes")
        handle_data(context=context, data=data)
    else:
        time.sleep(5)

