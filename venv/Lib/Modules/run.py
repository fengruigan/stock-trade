import alpaca_trade_api as tradeapi


class API:
    api = None

    def init_api(cls):
        cls.api = tradeapi.REST(keys._key, keys._secret_key, keys._base_url, api_version='v2')

class keys:
    _key = None
    _secret_key = None
    _base_url = 'https://paper-api.alpaca.markets'

    def set_keys(cls, key, secret_key):
        cls._key = key
        cls._secret_key = secret_key

    def get_keys(cls):
        return cls._key, cls._secret_key


class context:
    def __init__(cls):
        pass


class data:
    def current(cls, symbols, timeframe='1Min'):
        return API.api.get_barset(symbols=symbols, timeframe=timeframe, limit=1).df


    def history(cls, symbols, lookback=253, timeframe='1Min'):
        return API.api.get_barset(symbols=symbols, timeframe=timeframe, lookback=lookback).df