"""
This is the main script for backtesting
"""
from Lib.Backtest.run import API, keys, data
import pandas as pd
from Lib.Backtest.account import Account
from Lib.Backtest import execution as exe


keys.set_keys(keys, 'PKFE10XOBD7S4S5PYW4S', 'OQaJy/hcLjrNSNubTbUTpqbH21ybe/Dow65YYBfu')
API.init_api(API)

# exe.order("AAPL", 1, "buy")
# exe.order("AMZN", 1, "buy")
# exe.order("TSLA", 1, "buy")
# exe.order("GNUS", 10, "buy")
# print(Account.list_positions(Account))
# Account.close_all_positions(Account)
# print(Account.list_positions(Account))



time = pd.Timestamp('2019-07-16', tz='America/New_York').isoformat()
ti = '2019-07-15 15:59:00-04:00'
his = API.api.polygon.historic_agg_v2('AAPL', 1, 'minute', _from='2019-07-15', to='2019-07-15')
t = his[80].timestamp.isoformat()
print(his[80].timestamp)

curr = data.current(data, "AAPL", end=t)
# print(curr)
print(curr["AAPL"].close)
#
# px = API.api.get_barset('AMZN', limit=1, end=t, timeframe='1Min').df
# print(px)



# setup account info

# day function
# curr_day = start
# while (curr_day != end):
#     pass
#     # minute function
#     # handle data with timestamp input
# # calculate portfolio value
# curr_day = curr_day + day_progression







# print(time.isoformat())

# time = time + timeframe
# print(time.isoformat())


# api = tradeapi.REST('PK6Y5SRDKN61WWJXTMFK', 'qfgZ/029E5uXShxMFihldRyr4/qEQESe2L5gyYpD', api_version='v2')
# quote = api.polygon.historic_quotes_v2('AAPL', date='2020-06-11')

# quote = API.api.polygon.historic_quotes_v2("AAPL", "2020-06-10")[0]
# print(quote)

# aapl = API.api.polygon.historic_agg_v2('AAPL', 1, 'minute', _from='2017-01-01', to='2017-01-03')[500]
# time = aapl.timestamp
# print(time)

# times = (point.timestamp.ams8() for point in aapl if point.timestamp.hour in range(10, 16))
# for time in times:
#     print(time)

# stamp = API.api.polygon.historic_agg_v2('AAPL', 1, 'minute', _from='2017-01-04', to='2017-01-05')[1].timestamp.isoformat()

# time1 = aapl[0].timestamp
# time2 = aapl[1].timestamp
# time = time1.to_pydatetime()
# print(type(time))




# for point in aapl:
#     print(point.timestamp.hour)
# print(len(aapl))
# print(aapl.head())
# aapl['close'].plot()
# plt.show()

# quote = API.api.polygon.historic_quotes_v2('AAPL', '2017-01-05')[0].participant_timestamp.isoformat()
# print()
# print(len(quote))
# px = API.api.get_barset('AAPL', '1Min', limit=100, end=stamp).df
# px = API.api.get_barset('AAPL', '1Min', limit=100, start='2019-04-15T09:30:00-04:00', end='2019-04-20T09:30:00-04:00').df
# print(px)
# print(stamp)
# print(len(px))
# print(px.head())
# px['AAPL']['close'].plot()
# plt.show()
