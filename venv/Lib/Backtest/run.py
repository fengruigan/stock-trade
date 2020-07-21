"""
Contains the user configurations and system classes
"""

import alpaca_trade_api as tradeapi
import pandas as pd
# from Lib.Backtest.account import Account

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

class Context:
    securities = []
    params = {'trade_freq': 5}

    def __init__(cls):
        pass


class Data:
    curr_price = None
    curr_frame = dict((security, pd.DataFrame()) for security in Context.securities)
    data = None

    # def init_data(cls, start: str, timeframe):
    #     date = start - pd.to_timedelta('1 day')
    #     for security in Context.securities:
    #         cls.data[security] = API.api.polygon.historic_agg_v2(symbol=security, multiplier=1, timespan=timeframe, limit=Context.params['indicator_lookback'])

    def current(cls, symbol: str, curr_time:str, timeframe: str='1Min'):
        """
        Get the current barset at end date

        :param symbols: asset to look up
        :param end: end date ("current" date)
        :param timeframe: One of minute, 1Min, 5Min, 15Min, day or 1D. minute
               is an alias of 1Min. Similarly, day is of 1D.
        :return: pd.Series of length 1
        """
        if (not cls.data[symbol].truncate(after=curr_time).tail(1).empty):
            return cls.data[symbol].truncate(after=curr_time).tail(1)
        else:
            return pd.DataFrame()


    def history(cls, symbol: str, curr_time: str, lookback: int=253, timeframe: str='1Min'):
        """
        Get lookback number of barsets of historical data up to the end date

        :param symbols: asset to look up
        :param end: end date for historical data, needs to be in iso format pd.timestamp
        :param lookback: number of bars to get, from 1 to 1000
        :param timeframe: One of minute, 1Min, 5Min, 15Min, day or 1D. minute
               is an alias of 1Min. Similarly, day is of 1D.
        :return: pd.DataFrame of length lookback

        note: this is a modified version of the get_barset() in alpaca API.
              get_barset() allows for multiple symbols input, but it produces NaN data when the timestamps misalign
              so here I decided to make things less prone to error by taking symbol data one by one
        """
        # return API.api.get_barset(symbols=symbol, timeframe=timeframe, limit=lookback, end=end).df
        if (not cls.data[symbol].truncate(after=curr_time).tail(lookback).empty):
            return cls.data[symbol].truncate(after=curr_time).tail(lookback)
        else:
            return pd.DataFrame()


class Clock:
    """
    This clock will be create the time line for backtest
    """
    time_zone = 'America/New_York'
    start = "2017-01-01T00:00:00-05:00"
    end = "2018-01-01T00:00:00-05:00"
    timeframe = "minute"
    day_delta = pd.to_timedelta('1 day')
    minute_delta = pd.to_timedelta('1 minute')
    timeline = [] ##### make this a fixed list of timestamp with 1 min delta
    dateline = []
    curr_time = None
    curr_day = None
    time_idx = 0
    is_running = False

    def init_clock(cls, context, start: str, end: str, minute_delta: str='1 minute', timeframe: str='minute'):
        """
        initialize clock for backtest, generate the timeline for later use

        :param start: isoformat pd.timestamp
        :param end: isoformat pd.timestamp
        :param minute_delta: difference between minute level timestamps, usually set to be the trade_freq of the strategy
        :param timeframe: minute or day, determines the frequency of data acquisition
        :return:
        """
        cls.start = pd.Timestamp(start, tz=cls.time_zone)
        cls.end = pd.Timestamp(end, tz=cls.time_zone)
        cls.curr_day = cls.start
        cls.timeframe = timeframe
        cls.minute_delta = pd.to_timedelta(minute_delta)
        cls.timeline = []
        cls.dateline = []
        cls.time_idx = 0
        cls.is_running = True

        ## handle Data initialization
        day = cls.start
        frames = dict((security, []) for security in context.securities)
        Data.data = dict((security, None) for security in context.securities)
        Data.curr_price = dict((security, 0.0) for security in Context.securities)
        while (day <= cls.end):
            if (day.dayofweek == 5 or day.dayofweek == 6):
                day = day + cls.day_delta
                continue
            cls.dateline.append(day)
            cls.set_data_timeline(cls, context, day, frames)
            day = day + cls.day_delta

        cls.curr_time = cls.timeline[cls.time_idx]
        for security in context.securities:
            Data.data[security] = pd.concat(frames[security])
            Data.curr_frame[security] = Data.history(Data, security, cls.curr_time, Context.params['indicator_lookback'], cls.timeframe)
            print(security + ' has ' + str(len(Data.data[security])) + ' data points')

        # Data.curr_price = dict((security, float(Data.current(Data,security, cls.curr_time)[security].close)) for security in Context.securities)
        print('Initialize complete')



    def set_data_timeline(cls, context, day: str, frames):
        """
        append a list of minute timestamps to the class timeline
        :param day: current day
        :param minute_delta: difference between two timestamps
        :return:
        """
        start = day + pd.to_timedelta('9 hour 30 minute') ## skip to market open
        while (start != day + pd.to_timedelta('16 hour')):
            cls.timeline.append(start)
            start = start + pd.to_timedelta(cls.minute_delta)
        day = day.isoformat()
        for security in context.securities:
            frames[security].append(API.api.polygon.historic_agg_v2(symbol=security, multiplier=1, timespan=cls.timeframe,
                                                                    _from=day, to=day).df)


    def pass_time(cls, account):
        cls.time_idx = cls.time_idx + 1
        if (cls.time_idx < len(cls.timeline)):
            # print(cls.curr_time)
            cls.curr_time = cls.timeline[cls.time_idx]
            for security in Context.securities:
                try:
                    Data.curr_frame[security] = pd.concat([Data.curr_frame[security], Data.data[security].loc[str(Data.curr_frame[security].iloc[len(Data.curr_frame[security]) - 1].name) : str(cls.curr_time)].tail(-1)]).tail(Context.params['indicator_lookback'])
                except:
                    Data.curr_frame[security] = Data.history(Data, security, cls.curr_time, Context.params['indicator_lookback'], cls.timeframe)
                try:
                    Data.curr_price[security] = float(Data.curr_frame[security].tail(1).close)
                except:
                    Data.curr_price[security] = 0
                # if (len(Data.current(Data, security, cls.curr_time)) != 0):
                #     Data.curr_price[security] = float(Data.current(Data, symbol=security, curr_time=cls.curr_time).close)
                # else:
                #     Data.curr_price[security] = 0

            if (cls.curr_time.day != cls.curr_day):
                account.calculate_portfolio(account, cls.curr_time)
                account.portfolio_history.append(account.portfolio_value)
                # print('completed run for ' + cls.curr_day.isoformat())
                cls.curr_day = cls.curr_time.day
                # print(cls.curr_time.date())
            # account.benchmark.append(account.benchmark_value)
        else:
            cls.is_running = False

