"""
Contains the user configurations and system classes
"""

import alpaca_trade_api as tradeapi
import pandas as pd

"""
User config
"""

class API:
    api = None

    def init_api(cls):
        cls.api = tradeapi.REST(keys._key, keys._secret_key, keys._base_url, api_version='v2')

class keys:
    _key = None
    _secret_key = None
    _base_url = 'https://paper-api.alpaca.markets'

    def set_keys(cls, key: str, secret_key: str):
        cls._key = key
        cls._secret_key = secret_key

    def get_keys(cls):
        return cls._key, cls._secret_key

"""
System classes
"""

class context:
    def __init__(cls):
        pass


class data:
    def current(cls, symbol: str, end:str, timeframe: str='1Min'):
        """
        Get the current barset at end date

        :param symbols: asset to look up
        :param end: end date ("current" date)
        :param timeframe: One of minute, 1Min, 5Min, 15Min, day or 1D. minute
               is an alias of 1Min. Similarly, day is of 1D.
        :return: pd.Series of length 1
        """
        return API.api.get_barset(symbols=symbol, timeframe=timeframe, limit=1, end=end).df


    def history(cls, symbol: str, end:str, lookback: int=253, timeframe: str='1Min'):
        """
        Get lookback number of barsets of historical data up to the end date

        :param symbols: asset to look up
        :param end: end date for historical data, needs to be in iso format pd.timestamp
        :param lookback: number of bars to get, from 1 to 1000
        :param timeframe: One of minute, 1Min, 5Min, 15Min, day or 1D. minute
               is an alias of 1Min. Similarly, day is of 1D.
        :return: pd.Series of length lookback

        note: this is a modified version of the get_barset() in alpaca API.
              get_barset() allows for multiple symbols input, but it produces NaN data when the timestamps misalign
              so here I decided to make things less prone to error by taking symbol data one by one
        """
        return API.api.get_barset(symbols=symbol, timeframe=timeframe, limit=lookback, end=end).df

class Clock:
    """
    This clock will be create the time line for backtest
    """
    time_zone = 'America/New_York'
    start = "2017-01-01T00:00:00-05:00"
    end = "2018-01-01T00:00:00-05:00"
    timeframe = "minute"
    day_delta = pd.to_timedelta("1 day")
    timeline = [] ##### make this a fixed list of timestamp with 1 min delta
    curr_time = None

    def init_clock(cls, start: str, end: str, timeframe: str="minute"):
        """
        initialize clock for backtest, generate the timeline for later use

        :param start: isoformat pd.timestamp
        :param end: isoformat pd.timestamp
        :param timeframe: minute or day, determines the frequency of data acquisition
        :return:
        """
        cls.start = pd.Timestamp(start, tz=cls.time_zone)
        cls.end = pd.Timestamp(end, tz=cls.time_zone)
        cls.timeframe = timeframe
        day = pd.Timestamp(start)
        end = pd.Timestamp(end)
        while (day != end):
            if (day.dayofweek != 6 and day.dayofweek != 7):  ## skip weekends not skipping holidays
                cls.get_day_timeline(Clock, day)
            day = day + cls.day_delta


    def get_day_timeline(cls, day: str):
        start = day + pd.to_timedelta("9 hour 30 minute")
        minute_delta = pd.to_timedelta("1 minute")
        while (start <= (day + pd.to_timedelta("16 hour"))):
            cls.timeline.append(start.isoformat())
            start = start + minute_delta


    def get_time(cls):
        pass

