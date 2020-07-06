"""
module that handles order execution
"""
from Lib.Modules.user_config import keys
import alpaca_trade_api as tradeapi


api = tradeapi.REST(keys.key, keys.secret_key, keys.base_url, api_version="v2")

def order_value(symbol: str, value: float):
    """
    Create an order to specified asset for specified amount of value

    :param symbol: asset symbol
    :param value: desired amount to order
    :return: returns the id of the placed order if order was placed successfully

    Example:
        order_value("AAPL", 1000),
        if "AAPL"'s ask price is $300, 3 shares of "AAPL" will be placed with the id returned
    """
    if (api.get_account().regt_buying_power > value):
        askprice = api.get_last_quote(symbol).askprice
        if (askprice != 0):
            shares = int(value / askprice)
            return api.submit_order(symbol, shares, side="buy", type="market", time_in_force="gtc").id
        else:
            print("Error reading ask price, ask price = 0")
    else:
        print("Error placing order with order_value, not enough buying power")


def order_percent(symbol:str, percent:float):
    """
    Create an order to specified asset for amount based on the percent of the current portfolio

    :param symbol: asset symbol
    :param percent: desired percent to order
    :return: returns the id of the placed order if order was placed successfully

    Example:
        order_value("AAPL", 0.5),
        if "AAPL"'s ask price is $300 and current portfolio value is $1000,
        1 share of "AAPL" will be placed with the id returned
    """
    if (percent > 1):
        print("Percentage larger than 1, input smaller percentage")
        return
    value = api.get_account().portfolio_value * percent
    if (api.get_account().regt_buying_power > value):
        askprice = api.get_last_quote(symbol).askprice
        if (askprice != 0):
            shares = int(value / askprice)
            return api.submit_order(symbol, shares, side="buy", type="market", time_in_force="gtc").id
        else:
            print("Error reading ask price, ask price = 0")
    else:
        print("Error placing order with order_percent, not enough buying power")


def order_target():
    pass

def order_target_value():
    pass

def order_target_percent():
    pass