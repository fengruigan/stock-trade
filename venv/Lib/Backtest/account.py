"""
Holds the account info for backtests and handle order submission
"""

class Position:

    def __init__(self, symbol: str, qty: int):

        self.symbol = symbol
        self.qty = qty

    def set_qty(self, new_qty: int):
        self.qty = new_qty

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

    def init_account(cls, capital: int=100000, leverage: int=1):
        cls.portfolio_value = capital
        cls.buying_power = capital * leverage

    def calculate_portfolio(cls, timestamp: str):
        print("calculate portfolio")
        pass

    def submit_order(cls, symbol: str, qty: int, side: str, timestamp: str, type: str='market', time_in_force: str='gtc'):
        pos = cls.get_position(cls, symbol=symbol)
        if (side.__eq__('buy')):
            if pos:
                pos.set_qty(new_qty= pos.qty + qty)
                return
            else:
                cls.positions.append(Position(symbol, qty))
                return
        else:
            if pos:
                pos.set_qty(new_qty=pos.qty - qty)
                if (pos.qty - qty <= 0):
                    cls.positions.remove(pos)
                return
            else:
                print("Position of " + symbol + " does not exist")
                return
        # cls.calculate_portfolio(cls, timestamp)

    def list_positions(cls):
        return cls.positions

    def close_position(cls, symbol: str):
        """
        Liquidate specified asset if position exist

        :param symbol: specified asses
        :return:
        """
        pos = cls.get_position(cls, symbol=symbol)
        if pos:
            # calculate portfolio
            cls.positions.remove(pos)
        else:
            print("Position not found")

    def close_all_positions(cls):
        """
        Liquidate all positions

        :return:
        """
        for pos in cls.positions:
            # calculate portfolio
            pass
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
        # print("Position of " + symbol + " does not exist")
        return None








