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


# use this method to update user API keys
keys.update_key(keys, 'PKGQG65N7CIYQORL31FA', 'WMB/pHAMbNK7f8KV9WFh6UqJ6q9tKsS5b8UYtueQ')
api = tradeapi.REST(keys.key, keys.secret_key, keys.base_url, api_version='v2')

# running strategy
initialize(context=context)

# need to have a time control for handle_data
handle_data(context=context, data=data)
