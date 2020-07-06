import alpaca_trade_api as tradeapi


class keys:
    key = 'PKH1K1LTH0541LAZHXMT'
    secret_key = 'r/bnsex3KAFlxYgwM0Z0LtS4Vu3IqLsuPqRCEFEt'
    base_url = 'https://paper-api.alpaca.markets'

    def update_key(cls, key: str, secret_key: str):
        cls.key = key
        cls.secret_key = secret_key