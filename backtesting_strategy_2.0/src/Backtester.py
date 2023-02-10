import src.Holdings as hds
import src.StoplossStrategy as sls
import src.StoplossType as slt
import src.Strategy as str
import src.Results as rs

import datetime
from tqdm import tqdm # Adds progress bar during backtesting
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    filename='./tmp/backtest.log',
    filemode='w')

class Backtester:
    '''Performs the bulk of model manipulation by backtesting strategies
    on a given database and historical data.'''

    def __init__(self, db_name:str):
        '''
        Backtester Constructor
        db_name: the name of the postgres database (e.g. "seed")
        '''
        self._db_name = db_name

    def backtest(self, strategy: str.Strategy, start_date: datetime.datetime, stop_date: datetime.datetime, table_name: str, initial_assets=100):
        '''
        strategy: The strategy that's being tested
        start_date: The first day of the strategy (inclusive)
        stop_date: The stop date of the test (exclusive)
        table_name: The name of the table in the database that
            holds the data to backtest on
        '''

        results = rs.Results(db_name=self._db_name, initial_assets = initial_assets)
        strategy.set_db_name(self._db_name)
        strategy.set_table_name(table_name)

        # Generate list of relevant dates for the backtest
        date_list = [start_date + datetime.timedelta(days = day) for day in range((stop_date - start_date).days)]

        # For each date, rebalance or apply stoplosses as appropriate
        # Record which holdings are held afterward in the DB
        holdings = hds.Holdings(strategy.get_max_holdings())
        for i in tqdm (range(len(date_list)), desc="Backesting in progress..."):
            curr_date = date_list[i]
            logging.info("CURRENT DATE: " + curr_date.strftime('%m/%d/%Y'))
            
            # Re-evaluate all holdings or check for stoplosses
            if strategy.time_to_rebalance(start_date, curr_date):
                holdings = strategy.rebalance_holdings(holdings, curr_date)
            else: # Check current holdings for stoploss
                holdings = strategy.apply_stoplosses(holdings, start_date, curr_date)
            results.add_result(holdings, curr_date)

        # Complete the backtest
        results.finalize()