"""
module that handles order execution
"""
from Lib.Modules.user_config import keys
import alpaca_trade_api as tradeapi


api = tradeapi.REST(keys.key, keys.secret_key, keys.base_url, api_version="v2")

def order_value(symbol: str, value: float):
    askprice = api.get_last_quote(symbol).askprice
    if (askprice != 0):
        shares = int(value / askprice)
        return api.submit_order(symbol, shares, side="buy", type="market", time_in_force="gtc")
    else:
        print("Error reading ask price, ask price = 0")


def order_target():
    pass

def order_percent():
    pass

def order_target():
    pass

def order_target_value():
    pass

def order_target_percent():
    pass