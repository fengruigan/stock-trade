import numpy as np
import pandas as pd
import alpaca_trade_api as tradeapi


def ma(df):
    """
    This moving average will be primarily used for trading signals, not for plotting.
    Therefore we will only store the amount of data needed to calculate this ma and not more.
    """
    return df['close'].mean()
