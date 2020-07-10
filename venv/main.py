"""
This is the main python script
Handles api connection and main functions here
"""

import time
from Lib.Modules import indicators
from Lib.Modules import execution as exe
from Lib.Modules.run import API, keys, context, data
# from Lib.Strategies.strategies import initialize, handle_data
from Lib.Modules.indicators import bollinger_band, ema
from Lib.Strategies.bollinger import initialize, handle_data

# use this method to update user API keys
keys.set_keys(keys, 'PKGNT09BXAL6WN6GA0KX', 'zd5goUdqHV6gMdi7GVb0j0167bLxxY2VchVMu3Hp')
API.init_api(API)

# # running strategy
initialize(context=context)

# need to have a time control for handle_data
run_time = 0
curr_minute = API.api.get_clock().__getattr__('timestamp').minute
while (run_time < 1000000):
    if (API.api.get_clock().__getattr__('timestamp').minute != curr_minute):
        curr_minute = API.api.get_clock().__getattr__('timestamp').minute
        run_time = run_time + 1
        print("Strategy ran for " + str(run_time) + " minutes")
        handle_data(context=context, data=data)
    else:
        time.sleep(5) # add delay to prevent API request flood
