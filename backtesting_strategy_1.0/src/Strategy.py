from tracemalloc import stop
import src.Holdings as hds
import src.StoplossStrategy as sls
import src.StoplossType as slt

class Strategy:

    def __init__(self, max_holdings: int, days_between_rebalance: int, stoploss_type: slt.StoplossType, trailing_days:int = None):
        self._max_holdings = max_holdings
        self._days_between_rebalance = days_between_rebalance
        self._stoplossStrategy = sls.StoplossStrategy()
        if not self._stoplossStrategy.set_stoploss_type(stoploss_type, trailing_days):
            raise Exception("Error setting stoploss strategy. Ensure trailng_days is set to None if strategy type is NONE or ABSOLUTE and not None if TRAILING")
        
    def get_max_holdings(self):
        return self._max_holdings

    def get_days_between_rebalance(self):
        return self._days_between_rebalance

    def get_stoplossStrategy(self):
        return self._stoplossStrategy

    #Complete as appropriate: ______________________________________________________

    def calculate_stoploss_percentage(ticker: str) -> float:
        # TODO
        pass

    def next():
        # TODO
        pass

