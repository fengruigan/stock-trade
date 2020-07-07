import alpaca_trade_api as tradeapi

class keys:
    _key = None
    _secret_key = None
    _base_url = 'https://paper-api.alpaca.markets'

    def set_keys(cls, key, secret_key):
        cls._key = key
        cls._secret_key = secret_key

    def get_keys(cls):
        return cls._key, cls._secret_key

    # def update_key(cls, key: str):
    #     cls.key = key
    #     return cls.key
    #
    # def update_secret_key(cls, secret_key: str):
    #     cls.secret_key = secret_key
    #     return cls.key

class context:
    def __init__(cls):
        pass


class data:
    def current(cls, symbols, timeframe='1Min'):
        return api.get_barset(symbols=symbols, timeframe=timeframe, limit=1).df


    def history(cls, symbols, lookback=253, timeframe='1Min'):
        return api.get_barset(symbols=symbols, timeframe=timeframe, lookback=lookback).df