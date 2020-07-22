"""
Holds the account info for backtests and handle order submission
"""
from Lib.Backtest.run import Data, Clock


class Position:

    def __init__(self, symbol: str, qty: int, timestamp: str):

        self.symbol = symbol
        self.qty = qty
        self.calc_market_value(timestamp)

    def set_qty(self, new_qty: int):
        self.qty = new_qty

    def calc_market_value(self, timestamp: str):
        if (self.qty > 0):
            # price = float(Data.current(Data, self.symbol, timestamp)[self.symbol].close)
            price = Data.curr_price[self.symbol]
            self.market_value = price * self.qty
        else:
            self.market_value = 0.0

    def __repr__(self):
        return '{name}({attr})'.format(
            name=self.__class__.__name__,
            attr=self.__dict__
        )

class Account:

    positions = []
    portfolio_value = 0.0
    leverage = 1
    buying_power = 0.0
    portfolio_history = []
    benchmark = []


    def get_account(cls):
        return cls.portfolio_value, cls.buying_power

    def init_account(cls, capital: int=100000, leverage: int=1):
        cls.portfolio_history = []
        cls.portfolio_value = capital
        cls.buying_power = capital * leverage

        # setup benchmark
        bench = Data.set_benchmark(Data, start=Clock.start.isoformat(), end=Clock.end.isoformat())
        bench_mult = int(cls.portfolio_value / bench[0])
        cls.benchmark = bench * bench_mult

        # cls.portfolio_history.append(cls.portfolio_value)


    def calculate_portfolio(cls, timestamp: str):
        sum = cls.buying_power
        for pos in cls.positions:
            pos.calc_market_value(timestamp)
            sum = sum + pos.market_value
        cls.portfolio_value = sum

    def submit_order(cls, symbol: str, qty: int, side: str, timestamp: str, type: str='market', time_in_force: str='gtc'):
        pos = cls.get_position(cls, symbol=symbol)
        if (side.__eq__('buy')):
            if pos:
                pos.set_qty(new_qty= pos.qty + qty)
            else:
                cls.positions.append(Position(symbol, qty, timestamp))
            cls.buying_power = cls.buying_power - qty * Data.curr_price[symbol]
            return
        else:
            if pos:
                pos.set_qty(new_qty=pos.qty - qty)
                if (pos.qty - qty <= 0):
                    cls.close_position(cls, symbol, timestamp)
                    return
                else:
                    cls.buying_power = cls.buying_power + qty * Data.curr_price[symbol]
                    return


    def list_positions(cls):
        return cls.positions

    def close_position(cls, symbol: str, timestamp: str):
        """
        Liquidate specified asset if position exist

        :param symbol: specified asses
        :return:
        """
        pos = cls.get_position(cls, symbol=symbol)
        if pos:
            cls.calculate_portfolio(cls, timestamp)
            pos.calc_market_value(timestamp)
            cls.buying_power = cls.buying_power + pos.market_value
            cls.positions.remove(pos)
        else:
            print("Position not found")

    def close_all_positions(cls):
        """
        Liquidate all positions

        :return:
        """
        for pos in cls.positions:
            cls.calculate_portfolio(cls)
            cls.buying_power = cls.portfolio_value
        cls.positions = []
        return

    def get_position(cls, symbol: str):
        """
        Currently unused, think more about its possible implementation

        :param symbol: asset in question
        :return: Position object or None
        """
        for pos in cls.positions:
            if (symbol.__eq__(pos.symbol)):
                return pos
        return None