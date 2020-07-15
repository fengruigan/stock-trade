"""
module that handles order execution for backtests
"""
from Lib.Backtest.run import API, data
from Lib.Backtest.account import Account


def order(symbol: str, qty: int, side: str, timestamp: str, type: str="market", time_in_force: str="gtc"):
    """
    This method is a refactoring of the original alpaca submit_order() method

    :param symbol: asset symbol or ID
    :param qty: number of shares to order
    :param side: buy or sell
    :param type: market, limit, stop, or stop_limit
    :param time_in_force: day, gtc, opg, cls, ioc, fok
    :return:
    """
    return Account.submit_order(Account, symbol, qty, side, timestamp, type, time_in_force)


def order_value(symbol: str, value: float, timestamp: str):
    """
    Create an order to specified asset for specified amount of value

    :param symbol: asset symbol or ID
    :param value: desired amount to order
    :return:

    Example:
        order_value("AAPL", 1000),
        if "AAPL"'s ask price is $300, method will attempt to buy 3 shares of "AAPL" with order id returned
        order_value("AAPL", -1000),
        method will attempt to sell 3 shares of "AAPL" with order id returned
        if value is larger then position market value,
        method will close position (sell all) for "AAPL" with order id returned
    """
    if (value == 0):
        print("Order value cannot be 0")
        return
    elif (value > 0):
        if (Account.buying_power > value):
            askprice = data.current(data, symbol=symbol, end=timestamp)[symbol].close  # this askprice will just be a close price for simplicity sake
            if (askprice != 0):
                shares = int(value / askprice)
                if (shares <= 0):
                    print("Order value too low, attempting to buy $" + str(value) + " of " + symbol + ", but the askprice is $" + str(askprice))
                    return
                print("Placing order to buy " + str(shares) + " shares of " + symbol)
                return order(symbol, shares, "buy", timestamp)
            else:
                print("Error reading askprice of " + symbol + ", askprice = 0")
                return
        else:
            print("Error buying " + symbol + ", not enough buying power")
            return
    else:
        value = -value
        pos = Account.get_position(Account, symbol=symbol)
        if pos:
            if (value >= float(position.market_value)): ######################## this needs a rewrite
                return Account.close_position(Account, symbol)
            else:
                bidprice = data.current(data, symbol=symbol, end=timestamp)[symbol].close # this bidprice will just be a close price for simplicity sake
                if (bidprice != 0):
                    shares = int(value / bidprice)
                    if (shares == 0):
                        print("Order value too low, attempting to sell $" + str(value) + " of " + symbol + ", but the bidprice is $" + str(bidprice))
                        return
                    print("Placing order to sell " + str(shares) + " shares of " + symbol)
                    return order(symbol, shares, "sell", timestamp)
                else:
                    print("Error reading bidprice of " + symbol + ", bidprice = 0 ")
                    return
        else:
            print("Attempted to sell " + symbol + " but position not found")
            return


def order_percent(symbol: str, percent: float, timestamp: str):
    """
    Create an order to specified asset for amount based on the percent of the current portfolio

    :param symbol: asset symbol or ID
    :param percent: desired percent to order value between 0 and 1
    :return:

    Example:
        order_percent("AAPL", 0.5),
        if "AAPL"'s ask price is $300 and current portfolio value is $1000,
        method will attempt to buy 1 share of "AAPL" with order id returned
        order_percent("AAPL", -0.5),
        method will attempt to sell 1 share of "AAPL" with order id returned
    """
    if (abs(percent) > 1):
        print("Percentage larger than 100%, input smaller percentage")
        return
    if (percent == 0):
        print("Percentage cannot be 0%")
        return
    value = Account.portfolio_value * percent
    return order_value(symbol=symbol, value=value, timestamp=timestamp)


def order_target(symbol:str, target_share:int, timestamp: str):
    """
    Create orders to target the desired number of shares holding in portfolio

    :param symbol: asset symbol or ID
    :param share: the target_share share, if target_share is greater than holding, a buy order will be submitted, else
                  a sell order will be submitted
    :return:

    Example:
        order_target("AAPL", 10),
        if current position qty of "AAPL" is 15, method will attempt to sell 5 shares of "AAPL"
        if current position qty of "AAPL" is 5, method will attempt to buy 5 shares of "AAPL"
        returning the order id in both cases
    """
    pos = Account.get_position(Account, symbol=symbol)
    if pos:
        shares = target_share - int(pos.qty)
        if shares == 0:
            return
        elif shares > 0:
            if (data.current(data, symbol=symbol, end=timestamp)[symbol].close * shares < Account.buying_power):  # this askprice will just be a close price for simplicity sake
                print("Placing order to buy " + str(shares) + " shares of " + symbol)
                return order(symbol, shares, "buy", timestamp)
            else:
                print(
                    "Error buying " + str(shares) + " shares of " + symbol + ", not enough buying power")
                return
        else:
            print("Placing order to sell " + str(shares) + " shares of " + symbol)
            return order(symbol, -shares, "sell", timestamp)
    if (data.current(data, symbol=symbol, end=timestamp)[symbol].close * target_share < Account.buying_power):  # this askprice will just be a close price for simplicity sake
        print("Placing order to buy " + str(target_shares) + " shares of " + symbol)
        return order(symbol, target_share, "buy", timestamp)
    else:
        print("Error buying " + str(target_share) + " shares of " + symbol + ", not enough buying power")
        return


def order_target_value(symbol: str, target_value: float, timestamp: str):
    """
    Create an order to specified asset to target specified amount of value

    :param symbol: asset symbol or ID
    :param value: desired target amount to order
    :return:

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
        return
    pos = Account.get_position(Account, symbol=symbol)
    if pos:
        value = target_value - float(position.market_value)  ######################## this needs a rewrite
        return order_value(symbol=symbol, value=value, timestamp=timestamp)
    else:
        return order_value(symbol=symbol, value=target_value, timestamp=timestamp)


def order_target_percent(symbol: str, target_percent: float, timestamp: str):
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
        return
    if (target_percent < 0):
        print("Shorting is currently not supported")
        target_percent == 0
    pos = Account.get_position(Account, symbol=symbol)
    if (target_percent == 0):
        if pos:
            return Account.close_position(Account, symbol=symbol)
        else:
            return
    else:
        if pos:
            percent = target_percent - (float(position.market_value) / Account.portfolio_value)  ######################## this needs a rewrite
            return order_percent(symbol=symbol, percent=percent, timestamp=timestamp)
        else:
            return order_percent(symbol=symbol, percent=target_percent, timestamp=timestamp)