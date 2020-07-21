"""
This is the technical analysis indicators module, A wrapper for the TA-Lib
The hope of this module is to reduce the number of times we need to look at TA-Lib's API

The price data read from alpaca API's get_barset(symbol).symbol is a pandas.Series,
which can be input directly into the indicator methods below

There are a lot more indicators to import,
import more when needed
"""
import pandas as pd
import ta.trend
import ta.volatility
import bisect


def ema(close, period=12, fillna=False):
    """
    Exponential Moving Average

    :param close: pd.Series of close prices
    :param period: number of periods
    :param fillna: if true, fill nan values
    :return: the last value of pd.Series of ema features
    """
    return ta.trend.ema_indicator(close=close, n=period, fillna=fillna)[-1]


def sma(close, period=12, fillna=False):
    """
    Simple Moving Average

    :param close: pd.Series of close prices
    :param period: number of periods
    :param fillna: if true, fill nan values
    :return: the last value of pd.Series of sma features
    """
    return ta.trend.sma_indicator(close=close, n=period, fillna=fillna)[-1]


def macd(close, period_slow=26, period_fast=12, fillna=False):
    """
    Moving Average Convergence Divergence

    :param close: pd.Series of close prices
    :param period_slow: number of periods for slow ma
    :param period_fast: number of periods for fast ma
    :param fillna: if true, fill nan values
    :return: the last value of pd.Series of macd features
    """
    return ta.trend.macd(close=close, n_slow=period_slow, n_fast=period_fast, fillna=fillna)[-1]


def macd_signal(close, period_slow=26, period_fast=12, period_signal=9, fillna=False):
    """
    Moving Average Convergence Divergence (MACD Signal)
    Shows EMA of MACD.

    :param close: pd.Series of close prices
    :param period_slow: number of periods for slow ma
    :param period_fast: number of periods for fast ma
    :param period_signal: number of periods for signal
    :param fillna: if true, fill nan values
    :return: the last value of pd.Series of macd_signal features
    """
    return ta.trend.macd_signal(close=close, n_slow=period_slow, n_fast=period_fast, n_sign=period_signal, fillna=fillna)[-1]


def macd_diff(close, period_slow=26, period_fast=12, period_signal=9, fillna=False):
    """
    Moving Average Convergence Divergence (MACD Diff)
    Shows the relationship between MACD and MACD Signal.

    :param close: pd.Series of close prices
    :param period_slow: number of periods for slow ma
    :param period_fast: number of periods for fast ma
    :param period_signal: number of periods for signal
    :param fillna: if true, fill nan values
    :return: the last value of pd.Series of macd_diff features
    """
    return ta.trend.macd_diff(close=close, n_slow=period_slow, n_fast=period_fast, n_sign=period_signal, fillna=fillna)[-1]


def adx(px, period=14, fillna=False):
    """
    Average Directional Movement Index (ADX)

    :param px: pd.Series of prices
    :param period: number of periods
    :param fillna: if true, fill nan values
    :return: The last value in the pd.Series
    """
    return ta.trend.adx(high=px.high, low=px.low, close=px.close, n=period, fillna=fillna)[-1]


def fibonacci_support(px):
    """
        This method comes from blueshift_library

        Computes the current Fibonnaci support and resistance levels.
        Returns the distant of the last price point from both.
        Args:
            px (ndarray): input price array
        Returns:
            Tuple, distance from support and resistance levels.
    """

    def fibonacci_levels(px):
        return [min(px) + l * (max(px) - min(px)) for l in [0, 0.236, 0.382, 0.5, 0.618, 1]]

    def find_interval(x, val):
        return (-1 if val < x[0] else 99) if val < x[0] or val > x[-1] \
            else max(bisect.bisect_left(x, val) - 1, 0)

    last_price = px[-1]
    lower_dist = upper_dist = 0
    sups = fibonacci_levels(px[:-1])
    idx = find_interval(sups, last_price)

    if idx == -1:
        lower_dist = -1
        upper_dist = round(100.0 * (sups[0] / last_price - 1), 2)
    elif idx == 99:
        lower_dist = round(100.0 * (last_price / sups[-1] - 1), 2)
        upper_dist = -1
    else:
        lower_dist = round(100.0 * (last_price / sups[idx] - 1), 2)
        upper_dist = round(100.0 * (sups[idx + 1] / last_price - 1), 2)

    return lower_dist, upper_dist


def bollinger_band(volume, period=20, fillna=False):
    """
    Bollinger Band

    :param volume: volume data pd.Series
    :param period: period for bollinger band
    :return: The last value in upper, middle, and low band
    """

    def bollinger_mavg(close, n=20, fillna=False):
        """Bollinger Bands (BB)     Mid Band
        N-period simple moving average (MA).
        https://en.wikipedia.org/wiki/Bollinger_Bands
        Args:
            close(pandas.Series): dataset 'Close' column.
            n(int): n period.
            fillna(bool): if True, fill nan values.
        Returns:
            pandas.Series: New feature generated.
        """
        indicator = ta.volatility.BollingerBands(close=close, n=n, fillna=fillna)
        return indicator.bollinger_mavg()


    def bollinger_hband(close, n=20, ndev=2, fillna=False):
        """Bollinger Bands (BB)     Upper Band
        Upper band at K times an N-period standard deviation above the moving
        average (MA + Kdeviation).
        https://en.wikipedia.org/wiki/Bollinger_Bands
        Args:
            close(pandas.Series): dataset 'Close' column.
            n(int): n period.
            ndev(int): n factor standard deviation
            fillna(bool): if True, fill nan values.
        Returns:
            pandas.Series: New feature generated.
        """
        indicator = ta.volatility.BollingerBands(close=close, n=n, ndev=ndev, fillna=fillna)
        return indicator.bollinger_hband()


    def bollinger_lband(close, n=20, ndev=2, fillna=False):
        """Bollinger Bands (BB)     Lower Band
        Lower band at K times an N-period standard deviation below the moving
        average (MA − Kdeviation).
        https://en.wikipedia.org/wiki/Bollinger_Bands
        Args:
            close(pandas.Series): dataset 'Close' column.
            n(int): n period.
            ndev(int): n factor standard deviation
            fillna(bool): if True, fill nan values.
        Returns:
            pandas.Series: New feature generated.
        """
        indicator = ta.volatility.BollingerBands(close=close, n=n, ndev=ndev, fillna=fillna)
        return indicator.bollinger_lband()

    upper = bollinger_hband(close=volume, n=period, fillna=fillna)
    mid = bollinger_mavg(close=volume, n=period, fillna=fillna)
    lower = bollinger_lband(close=volume, n=period, fillna=fillna)
    return upper[-1], mid[-1], lower[-1]