import src.Holdings as hds
import src.StoplossStrategy as sls
import src.StoplossType as slt
import datetime

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

    def time_to_reevaluate(self, start_date, current_date) -> bool:
        time_difference = current_date - start_date
        days_elapsed = time_difference.days
        return (days_elapsed % self._days_between_rebalance) == 0

    #Complete as appropriate: ______________________________________________________

    def reevaluate_holdings(holdings: hds.Holdings, current_date) -> hds.Holdings: # Should uninverse pass???
        assert holdings.get_current_holdings_number == 0
        # implement as necessary

    def calculate_stoploss_percentage(ticker: str) -> float:
        # TODO
        pass

