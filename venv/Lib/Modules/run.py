import alpaca_trade_api as tradeapi


class keys:
    key = 'PKH1K1LTH0541LAZHXMT'
    secret_key = 'r/bnsex3KAFlxYgwM0Z0LtS4Vu3IqLsuPqRCEFEt'
    base_url = 'https://paper-api.alpaca.markets'

    def update_key(cls, key: str, secret_key: str):
        cls.key = key
        cls.secret_key = secret_key


class context:
    def __init__(cls):
        pass


class data:
    def current(cls, symbols, timeframe='1Min'):
        return api.get_barset(symbols=symbols, timeframe=timeframe, limit=1).df


    def history(cls, symbols, lookback=253, timeframe='1Min'):
        return api.get_barset(symbols=symbols, timeframe=timeframe, lookback=lookback).df