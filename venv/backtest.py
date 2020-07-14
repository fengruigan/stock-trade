"""
This is the main script for backtesting
"""
from Lib.Modules.run import API, keys
import pandas as pd
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt


keys.set_keys(keys, 'PK6Y5SRDKN61WWJXTMFK', 'qfgZ/029E5uXShxMFihldRyr4/qEQESe2L5gyYpD')
API.init_api(API)

time_zone = 'America/New_York'
start = pd.Timestamp("2017-01-01", tz=time_zone)
end = pd.Timestamp("2018-01-01", tz=time_zone)
day_progression = pd.to_timedelta("1 day")

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

time = pd.Timestamp('2017-01-03 14:55:00-05:00')
print(time)
quotes = API.api.polygon.historic_quotes_v2("AAPL", time, reverse=True)
# print(quotes[0].participant_timestamp)
# for quote in quotes:
    # print(quote.participant_timestamp.hour)
    # if quote.participant_timestamp.hour == 12:
    #     print(quote.participant_timestamp.hour)
    #     print(quote)
    #     break

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
