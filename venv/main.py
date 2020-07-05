import requests
import json
import numpy as np
import alpaca_trade_api as tradeapi


key = 'PKSJQXDQJO4C11AB2HG6'
secret_key = 'dZ9V3fiTxy7fzzlb1DTuEpsIkJuRRRdvsyKILkwO'
base_url = 'https://paper-api.alpaca.markets'
api = tradeapi.REST(key, secret_key, base_url, api_version='v2')
api.submit_order(symbol="AAPL", qty=1, side="buy", type="market", time_in_force="gtc")




