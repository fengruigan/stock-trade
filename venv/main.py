"""
This is the main python script
Handles api connection and main functions here
"""

import time
from Lib.Modules import indicators
from Lib.Modules import execution as exe
from Lib.Modules.run import API, Keys, Context, Data
from Lib.Strategies.strategies import initialize, handle_data
# from Lib.Strategies.bollinger import initialize, handle_data
import pandas as pd

# use this method to update user API keys
alpaca_key = 'PK37ODJ81HJIFAHS6O86'
alpaca_secret_key = 'j68RM2mO7AiIUwAjcNk6A5Hiwgn3LoTqmpcH/KDG'

Keys.set_keys(Keys, alpaca_key, alpaca_secret_key)
API.init_api(API)

# # running strategy
initialize(context=Context)

# need to have a time control for handle_data
run_time = 0
curr_minute = API.api.get_clock().__getattr__('timestamp').minute
print("Up and running")
while (run_time < 43200):  # time is set to be one month from now
    if (not API.api.get_clock().is_open):
        print("Sleeping till market open")
        time.sleep((API.api.get_clock().next_open - API.api.get_clock().timestamp).seconds + 10)
    if (API.api.get_clock().__getattr__('timestamp').minute != curr_minute):
        curr_minute = API.api.get_clock().__getattr__('timestamp').minute
        run_time = run_time + 1
        # print("Strategy ran for " + str(run_time) + " minutes")
        handle_data(context=context, data=Data)
    else:
        time.sleep(5) # add delay to prevent API request flood
