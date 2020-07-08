"""
This is the main python script
Handles api connection and main functions here
"""
from Lib.Modules import indicators
from Lib.Modules import execution as exe
from Lib.Modules.run import API, keys, context, data
# from Lib.Strategies.strategies import initialize, handle_data
from Lib.Strategies.test import initialize, handle_data
from Lib.Modules.indicators import fibonacci_support, adx
import time



# use this method to update user API keys
keys.set_keys(keys, 'PKHDD32BIDCMMLAN59WI', 'U50Ch0jCc/UcTj98rC0OGjSAMMyfwCJ/pvoZW5ts')
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
# handle_data(context=context, data=data)

symbol = 'BILI'
px = data.history(data, symbol, 375)[symbol]
lower, upper = fibonacci_support(px.close)
ind2 = adx(px, 120)

print("lower = " + str(lower))
print("upper = " + str(upper))
print("ind2 = " + str(ind2))