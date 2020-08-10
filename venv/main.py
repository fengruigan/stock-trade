"""
This is the main python script
Handles api connection and main functions here
"""
import time
from Lib.Modules.run import API, Keys, Context, Data
from Lib.Strategies.strategies import initialize, handle_data
import pandas as pd


def trading_procedure():
    # use this method to update user API keys
    alpaca_key = 'PK37ODJ81HJIFAHS6O86'
    alpaca_secret_key = 'j68RM2mO7AiIUwAjcNk6A5Hiwgn3LoTqmpcH/KDG'

    Keys.set_keys(Keys, alpaca_key, alpaca_secret_key)
    API.init_api(API)

    # # running strategy
    initialize(context=Context)

    # need to have a time control for handle_data
    curr_date = pd.Timestamp(time.ctime()).date()
    end_date = curr_date + pd.to_timedelta("31 day")
    curr_minute = API.api.get_clock().__getattr__('timestamp').minute
    print("Up and running")
    while (curr_date <= end_date):  # time is set to be 31 days from now
        if (not API.api.get_clock().is_open):
            print("Sleeping till market open")
            try:
                time.sleep((API.api.get_clock().next_open - API.api.get_clock().timestamp).seconds + 10)
                curr_date = pd.Timestamp(time.ctime()).date()
                print("Running trading procedure for " + curr_date.isoformat())
            except:
                time.sleep(5)
        if (API.api.get_clock().__getattr__('timestamp').minute != curr_minute):
            curr_minute = API.api.get_clock().__getattr__('timestamp').minute
            # print("Strategy ran for " + str(run_time) + " minutes")
            handle_data(context=Context, data=Data)
        else:
            time.sleep(5) # add delay to prevent API request flood


if __name__ == "__main__":
    trading_procedure()
    print("Trading procedure has ended on date " + curr_date.isoformat())
    # maybe a sys.exit() here, otherwise heroku might try to restart the script?