"""
test backtest strategy
Data timeframe: minute
"""
from Lib.Backtest.run import Clock
from Lib.Backtest.account import Account
from Lib.Backtest.execution import order_target_percent
from Lib.Modules.indicators import fibonacci_support, adx


def initialize(context):
    """
        A function to define things to do at the start of the strategy
    """
    # universe selection
    context.securities = ['AMZN', 'AAPL']

    # define strategy parameters
    context.params = {'indicator_lookback':375,
                      'indicator_freq':'1Min',
                      'buy_signal_threshold':0.5,
                      'sell_signal_threshold':-0.5,
                      'ADX_period':120,
                      'trade_freq':5,
                      'leverage':1}

    # variables to track signals and target portfolio
    context.signals = dict((security,0) for security in context.securities)
    context.target_position = dict((security,0) for security in context.securities)


def handle_data(context, data):
    """
        A function to define things to do at every bar
    """
    # time to trade, call the strategy function
    run_strategy(context, data)
    Clock.pass_time(Clock, Account)

def run_strategy(context, data):
    """
        A function to define core strategy steps
    """
    generate_signals(context, data)
    generate_target_position(context, data)
    rebalance(context, data)

def rebalance(context,data):
    """
        A function to rebalance - all execution logic goes here
    """
    for security in context.securities:
        order_target_percent(security, context.target_position[security], Clock.curr_time)

def generate_target_position(context, data):
    """
        A function to define target portfolio
    """
    num_secs = len(context.securities)
    weight = round(1.0/num_secs,2)*context.params['leverage']

    for security in context.securities:
        if context.signals[security] > context.params['buy_signal_threshold']:
            context.target_position[security] = weight
        elif context.signals[security] < context.params['sell_signal_threshold']:
            # context.target_position[security] = -weight
            context.target_position[security] = 0
        else:
            context.target_position[security] = 0

def generate_signals(context, data):
    """
        A function to define define the signal generation
    """
    # try:
    #     price_data = data.history(data, context.securities,
    #         context.params['indicator_lookback'], context.params['indicator_freq'])
    # except:
    #     print("error here!!!!!!!")
    #     return

    for security in context.securities:
        try:
            px = data.history(data, security, Clock.curr_time, context.params['indicator_lookback'], context.params['indicator_freq'])
        except:
            print("error here!!!!!!!")
            return
        # px = price_data[security]
        if (len(px) < context.params['indicator_lookback']):
            return
        context.signals[security] = signal_function(px, context.params, context.signals[security])
        # print(security + " has signal " + str(context.signals[security]))

def signal_function(px, params, last_signal):
    """
        The main trading logic goes here, called by generate_signals above
    """
    lower, upper = fibonacci_support(px.close)
    ind2 = adx(px, params['ADX_period'])

    if lower == -1:
        return -1
    elif upper == -1:
        return 1
    elif upper > 0.02 and lower > 0 and upper/lower > 3 and ind2 < 20:
        return -1
    elif lower > 0.02 and upper > 0 and lower/upper > 3 and ind2 < 20:
        return 1
    else:
        return last_signal
