"""
Test strategy
"""
import  alpaca_trade_api as tradeapi
from Lib.Modules.execution import order_target_percent


def initialize(context):

    context.securities = ['AAPL', 'AMZN','BILI']
    context.params = {'trade_freq': 2}

    context.bar_count = 0

    context.target_position = dict((security, 1 / len(context.securities)) for security in context.securities)


def handle_data(context, data):
    context.bar_count = context.bar_count + 1
    if context.bar_count < context.params['trade_freq']:
        return

    # time to trade, call the strategy function
    context.bar_count = 0
    rebalance(context)

def rebalance(context):
    for security in context.securities:
        order_target_percent(security, context.target_position[security])