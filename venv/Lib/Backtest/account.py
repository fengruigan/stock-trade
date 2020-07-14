"""
Holds the account info for backtests and handle order submission
"""

class account:
    positions = []
    portfolio_value = 0
    leverage = 1
    buying_power = 0

    def set_capital(cls, qty: int=100000, leverage: int=1):
        cls.portfolio_value = qty
        cls.buying_power = qty * leverage

    def calculate_portfolio(cls):
        pass

    def submit_order(cls, symbol: str, qty: int, side: str, type: str='market', time_in_force: str='gtc'):
        pass

    def list_positions(cls):
        return cls.positions

    def get_position(cls, symbol: str):
        try:
            return positions[symbol]
        except:
            print("Position of " + symbol + " does not exist")
            return []



