import src.Holdings as hds
import src.StoplossStrategy as sls
import src.StoplossType as slt
import src.Strategy as str
import datetime

class Backtester:

    def __init__(self):
        pass

    def backtest(self, strategy: str.Strategy, start_date, stop_date):
        '''strategy - The strategy under test
        The first day of the strategy (inclusive)
        The stop date of the test (exclusive)
        '''

        # Generate list of relevant dates for the backtest
        date_list = [start_date + datetime.timedelta(days = day) for day in range((stop_date - start_date).days)]

        uniqueBacktestID = 0 # generate unique backtest ID that's tied to where results of backtedst are stored in the DB

        # For each date, determine what action to take according to the Strategy
        # Take that action, getting a new list of holdings
        # Store changes in the DB
        for curr_date in date_list:
            new_holdings = None
            if strategy.time_to_reevaluate(start_date, curr_date): # Re-evaluate all holdings
                strategy.reevaluate_holdings(curr_date)
            else: # Check current holdings for stoploss
                strategy.apply_stoplosses(curr_date)
            # Log the changes
            # log (holdings, new_holdings, curr_date, reevaluated: Bool) for later analysis/visualization

        results = strategy.complete()
        return results
        # return uniqueBacktestID # Return backtestID