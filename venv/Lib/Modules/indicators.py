"""
This is the technical analysis indicators module, A wrapper for the TA-Lib
The hope of this module is to reduce the number of times we need to look at TA-Lib's API

The price data read from alpaca API's get_barset(symbol).symbol is a pandas.Series,
which can be input directly into the indicator methods below

There are a lot more indicators to import,
import more when needed
"""
import pandas as pd
import alpaca_trade_api as tradeapi
import ta.trend


def ema(close, period=12, fillna=False):
    """
    Exponential Moving Average

    :param close: pd.Series of close prices
    :param period: number of periods
    :param fillna: if true, fill nan values
    :return: pd.Series of ema features
    """
    return ta.trend.ema_indicator(close=close, periods=period, fillna=fillna)


def sma(close, period=12, fillna=False):
    """
    Simple Moving Average

    :param close: pd.Series of close prices
    :param period: number of periods
    :param fillna: if true, fill nan values
    :return: pd.Series of sma features
    """
    return ta.trend.sma_indicator(close=close, n=period, fillna=fillna)


def macd(close, period_slow=26, period_fast=12, fillna=False):
    """
    Moving Average Convergence Divergence

    :param close: pd.Series of close prices
    :param period_slow: number of periods for slow ma
    :param period_fast: number of periods for fast ma
    :param fillna: if true, fill nan values
    :return: pd.Series of macd features
    """
    return ta.trend.macd(close=close, n_slow=period_slow, n_fast=period_fast, fillna=fillna)


def macd_signal(close, period_slow=26, period_fast=12, period_signal=9, fillna=False):
    """
    Moving Average Convergence Divergence (MACD Signal)
    Shows EMA of MACD.

    :param close: pd.Series of close prices
    :param period_slow: number of periods for slow ma
    :param period_fast: number of periods for fast ma
    :param period_signal: number of periods for signal
    :param fillna: if true, fill nan values
    :return: pd.Series of macd_signal features
    """
    return ta.trend.macd_signal(close=close, n_slow=period_slow, n_fast=period_fast, n_sign=period_signal, fillna=fillna)


def macd_diff(close, period_slow=26, period_fast=12, period_signal=9, fillna=False):
    """
    Moving Average Convergence Divergence (MACD Diff)
    Shows the relationship between MACD and MACD Signal.

    :param close: pd.Series of close prices
    :param period_slow: number of periods for slow ma
    :param period_fast: number of periods for fast ma
    :param period_signal: number of periods for signal
    :param fillna: if true, fill nan values
    :return: pd.Series of macd_diff features
    """
    return ta.trend.macd_diff(close=close, n_slow=period_slow, n_fast=period_fast, n_sign=period_signal, fillna=fillna)


def adx(high, low, close, period=14, fillna=False):
    """
    Average Directional Movement Index (ADX)

    :param high: pd.Series of high prices
    :param low: pd.Series of low prices
    :param close: pd.Series of close prices
    :param period: number of periods
    :param fillna: if true, fill nan values
    :return: pd.Series of adx features
    """
    return ta.trend.adx(high=high, low=low, close=close, n=period, fillna=fillna)