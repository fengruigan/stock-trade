"""
This is the main python script
Handles api connection and main functions here
"""

import time
from Lib.Modules import indicators
from Lib.Modules import execution as exe
from Lib.Modules.run import API, keys, context, data
from Lib.Modules.indicators import fibonacci_support, adx
from Lib.Strategies.strategies import initialize, handle_data



# use this method to update user API keys
keys.set_keys(keys, 'PK6A0GIRDVVFYYMOCAEV', 'WugXyNdln6WUJhkvSPAJGw26ozMioPG2864C3xV/')
API.init_api(API)

# # running strategy
initialize(context=context)

# need to have a time control for handle_data
run_time = 0
curr_minute = API.api.get_clock().__getattr__('timestamp').minute
# while (run_time < 1000000):
#     if (API.api.get_clock().__getattr__('timestamp').minute != curr_minute):
#         curr_minute = API.api.get_clock().__getattr__('timestamp').minute
#         run_time = run_time + 1
#         print("Strategy ran for " + str(run_time) + " minutes")
#         handle_data(context=context, data=data)
#     else:
#         time.sleep(5)
