"""
    Title: Bollinger Band Strategy (NSE)
    Description: This is a long short strategy based on bollinger bands
        and SMA dual signals
    Style tags: Systematic Fundamental
    Asset class: Equities, Futures, ETFs and Currencies
    Dataset: NSE Minute
"""
from Lib.Modules.indicators import bollinger_band, ema
from Lib.Modules.execution import order_target_percent

def initialize(context):
    """
        A function to define things to do at the start of the strategy
    """
    # universe selection
    context.securities = ['BA', 'LUV']

    # define strategy parameters
    context.params = {'indicator_lookback': 375,
                      'indicator_freq': '1Min',
                      'buy_signal_threshold': 0.5,
                      'sell_signal_threshold': -0.5,
                      'SMA_period_short': 15,
                      'SMA_period_long': 60,
                      'BBands_period': 300,
                      'trade_freq': 1,
                      'leverage': 1}

    # variable to control trading frequency
    context.bar_count = 0

    # variables to track signals and target portfolio
    context.signals = dict((security, 0) for security in context.securities)
    context.target_position = dict((security, 0) for security in context.securities)



    # schedule_function(rebalance,
    #                   date_rules.every_day(),
    #                   time_rules.every_minute())


def handle_data(context, data):
    """
        A function to define things to do at every bar
    """
    context.bar_count = context.bar_count + 1
    if context.bar_count < context.params['trade_freq']:
        return

    # time to trade, call the strategy function
    context.bar_count = 0
    run_strategy(context, data)


def run_strategy(context, data):
    """
        A function to define core strategy steps
    """
    generate_signals(context, data)
    generate_target_position(context, data)
    rebalance(context, data)


def rebalance(context, data):
    """
        A function to rebalance - all execution logic goes here
    """
    for security in context.securities:
        order_target_percent(security, context.target_position[security])


def generate_target_position(context, data):
    """
        A function to define target portfolio
    """
    num_secs = len(context.securities)
    weight = round(1.0 / num_secs, 2) * context.params['leverage']

    for security in context.securities:
        if context.signals[security] > context.params['buy_signal_threshold']:
            context.target_position[security] = weight
        elif context.signals[security] < context.params['sell_signal_threshold']:
            context.target_position[security] = -weight
        else:
            context.target_position[security] = 0


def generate_signals(context, data):
    """
        A function to define define the signal generation
    """
    for security in context.securities:
        try:
            px = data.history(security,
                                      context.params['indicator_lookback'],
                                      context.params['indicator_freq'])[security].close
            vx = data.history(security,
                                       context.params['indicator_lookback'],
                                       context.params['indicator_freq'])[security].volume
            context.signals[security] = signal_function(px, vx, context.params)
        except:
            return


def signal_function(px, vx, params):
    """
        The main trading logic goes here, called by generate_signals above
    """
    upper, mid, lower = bollinger_band(vx, params['BBands_period'])
    ind2 = ema(px, params['SMA_period_short'])
    ind3 = ema(px, params['SMA_period_long'])
    last_vx = vx[-1]
    dist_to_upper = 100 * (upper - last_vx) / (upper - lower)

    if dist_to_upper > 90 and ind2 - ind3 > 0:
        return 1
    elif ind2 - ind3 < 0 and dist_to_upper > 65:
        return -1
    else:
        return 0