import src.Holdings as hds
import src.StoplossStrategy as sls
import src.StoplossType as slt
import src.Strategy as str
import src.Results as rs

import datetime
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(message)s',
      filename='./tmp/backtest.log',
      filemode='w')

class Backtester:

    def __init__(self, db_name:str):
        self._db_name = db_name

    def backtest(self, strategy: str.Strategy, start_date, stop_date, table_name: str, initial_assets=100):
        '''strategy - The strategy under test
        The first day of the strategy (inclusive)
        The stop date of the test (exclusive)
        '''

        results = rs.Results(db_name=self._db_name, initial_assets = initial_assets)
        strategy.set_db_name(self._db_name)
        strategy.set_table_name(table_name)

        # Generate list of relevant dates for the backtest
        date_list = [start_date + datetime.timedelta(days = day) for day in range((stop_date - start_date).days)]

        # For each date, rebalance or apply stoplosses as appropriate
        # Record which holdings are held afterward in the DB
        for i in tqdm (range(len(date_list)), desc="Backesting in progress..."):
            curr_date = date_list[i]
            logging.info("CURRENT DATE: " + curr_date.strftime('%m/%d/%Y'))
            
            strategy_holdings = None
            # Re-evaluate all holdings
            if strategy.time_to_rebalance(start_date, curr_date):
                strategy_holdings = strategy.rebalance_holdings(curr_date)
            # Check current holdings for stoploss
            else:
                strategy_holdings = strategy.apply_stoplosses(start_date, curr_date)
            results.add_result(strategy_holdings, curr_date)

        # Complete the backtest
        results.finalize()