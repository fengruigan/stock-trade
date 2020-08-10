"""
module that handles order execution

Most order methods does not take into account open orders
Therefore, consider canceling all open orders before placing new ones
or wait for orders to be filled

I think I will put order check in strategies section
"""
from Lib.Modules.run import API


def order(symbol: str, qty: int, side: str, type: str="market", time_in_force: str="gtc"):
    """
    This method is a refactoring of the original alpaca submit_order() method

    :param symbol: asset symbol or ID
    :param qty: number of shares to order
    :param side: buy or sell
    :param type: market, limit, stop, or stop_limit
    :param time_in_force: day, gtc, opg, cls, ioc, fok
    :return: returns order id
    """
    return API.api.submit_order(symbol, qty, side, type, time_in_force).id


def order_value(symbol: str, value: float):
    """
    Create an order to specified asset for specified amount of value

    :param symbol: asset symbol or ID
    :param value: desired amount to order
    :return: returns the id of the placed order if order was placed successfully

    Example:
        order_value("AAPL", 1000),
        if "AAPL"'s ask price is $300, method will attempt to buy 3 shares of "AAPL" with order id returned
        order_value("AAPL", -1000),
        method will attempt to sell 3 shares of "AAPL" with order id returned
        if value is larger then position market value,
        method will close position (sell all) for "AAPL" with order id returned
    """
    if (value == 0):
        # print("Order value cannot be 0")
        return None
    elif (value > 0):
        if (float(API.api.get_account().buying_power) >= value):
            askprice = API.api.get_last_quote(symbol).askprice
            if (askprice != 0):
                shares = int(value / askprice)
                if (shares <= 0):
                    # print("Order value too low, attempting to buy $" + str(value) + " of " + symbol + ", but the askprice is $" + str(askprice))
                    return None
                print("Placing order to buy " + str(shares) + " shares of " + symbol)
                return order(symbol, shares, "buy")
            else:
                # print("Error reading askprice of " + symbol + ", askprice = 0")
                return None
        else:
            # print("Error buying " + symbol + ", not enough buying power")
            return None
    else:
        value = -value
        try:
            posiiton = API.api.get_position(symbol=symbol)
        except:
            # print("Attempted to sell " + symbol + " but position not found")
            return None
        if (value >= float(position.market_value)):  # position.market_value should be get_last_quote(symbol) instead?
            qty = position.qty
            print("Selling " + str(qty) + " shares of " + symbol + ", position closed")
            return API.api.close_position(symbol).id
        else:
            bidprice = API.api.get_last_quote(symbol).bidprice
            if (bidprice != 0):
                shares = int(value / bidprice)
                if (shares == 0):
                    # print("Order value too low, attempting to sell $" + str(value) + " of " + symbol + ", but the bidprice is $" + str(bidprice))
                    return None
                print("Placing order to sell " + str(shares) + " shares of " + symbol)
                return order(symbol, shares, "sell")
            else:
                # print("Error reading bidprice of " + symbol + ", bidprice = 0 ")
                return None


def order_percent(symbol:str, percent:float):
    """
    Create an order to specified asset for amount based on the percent of the current portfolio

    :param symbol: asset symbol or ID
    :param percent: desired percent to order value between 0 and 1
    :return: returns the id of the placed order if order was placed successfully

    Example:
        order_percent("AAPL", 0.5),
        if "AAPL"'s ask price is $300 and current portfolio value is $1000,
        method will attempt to buy 1 share of "AAPL" with order id returned
        order_percent("AAPL", -0.5),
        method will attempt to sell 1 share of "AAPL" with order id returned
    """
    if (abs(percent) > 1):
        print("Percentage larger than 100%, input smaller percentage")
        return None
    if (percent == 0):
        print("Percentage cannot be 0%")
        return None
    value = float(API.api.get_account().portfolio_value) * percent
    return order_value(symbol, value)


def order_target(symbol:str, target_share:int):
    """
    Create orders to target the desired number of shares holding in portfolio

    :param symbol: asset symbol or ID
    :param share: the target_share share, if target_share is greater than holding, a buy order will be submitted, else
                  a sell order will be submitted
    :return: returns the id of the placed order if order was placed successfully

    Example:
        order_target("AAPL", 10),
        if current position qty of "AAPL" is 15, method will attempt to sell 5 shares of "AAPL"
        if current position qty of "AAPL" is 5, method will attempt to buy 5 shares of "AAPL"
        returning the order id in both cases
    """
    try:
        position = API.api.get_position(symbol=symbol)
    except:
        if (API.api.get_last_quote(symbol).askprice * target_share < float(API.api.get_account().buying_power)):
            print("Placing order to buy " + str(target_shares) + " shares of " + symbol)
            return order(symbol, target_share, "buy")
        else:
            # print("Error buying " + str(target_share) + " shares of " + symbol + ", not enough buying power")
            return None
    shares = target_share - int(position.qty)
    if shares == 0:
        return None
    elif shares > 0:
        if (API.api.get_last_quote(symbol).askprice * shares < float(API.api.get_account().buying_power)):
            print("Placing order to buy " + str(shares) + " shares of " + symbol)
            return order(symbol, shares, "buy")
        else:
            # print("Error buying " + str(shares) + " shares of " + symbol + ", not enough buying power")
            return None
    else:
        print("Placing order to sell " + str(shares) + " shares of " + symbol)
        return order(symbol, -shares, "sell")



def order_target_value(symbol: str, target_value: float):
    """
    Create an order to specified asset to target specified amount of value

    :param symbol: asset symbol or ID
    :param value: desired target amount to order
    :return: returns the id of the placed order if order was placed successfully

    Example:
        order_target_value("AAPL", 1000),
        if current position market value of "AAPL" is 500 and "AAPL"'s ask price is $300,
        method will attempt to buy 1 share of "AAPL";
        if current position market value of "AAPL" is 1500,
        method will attempt to sell 1 share of "AAPL";
        if currently not holding any share of "AAPL", method will attempt to buy 3 shares of "AAPL"
    """
    if (target_value <= 0):
        print("Target_value must be > 0")
        return None
    try:
        position = API.api.get_position(symbol=symbol)
    except:
        return order_value(symbol, target_value)
    value = target_value - float(position.market_value)  # position.market_value should be get_last_quote(symbol) instead?
    return order_value(symbol, value)



def order_target_percent(symbol: str, target_percent: float):
    """
    Create an order to specified asset to target amount based on the percent of the current portfolio

    :param symbol: asset symbol or ID
    :param percent: desired target percent to order value between 0 and 1
    :return: returns the id of the placed order if order was placed successfully

    Example:
        order_value("AAPL", 0.5),
        if "AAPL"'s ask price is $300 and current portfolio value is $1000,
        1 share of "AAPL" will be placed with the id returned
    """
    if (target_percent > 1):
        print("Percentage larger than 100%, input smaller target_percent")
        return None
    if (target_percent < 0):
        print("Shorting is currently not supported")
        target_percent == 0
    if (target_percent == 0):
        try:
            position = API.api.get_position(symbol=symbol)
        except:
            return None
        qty = position.qty
        print("Selling " + str(qty) + " shares of " + symbol + ", position closed")
        return API.api.close_position(symbol).id
    try:
        position = API.api.get_position(symbol=symbol)
    except:
        return order_percent(symbol, target_percent)
    percent = target_percent - (float(position.market_value) / float(API.api.get_account().portfolio_value)) # position.market_value should be get_last_quote(symbol) instead?
    return order_percent(symbol, percent)
