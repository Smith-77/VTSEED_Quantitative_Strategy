import src.Holdings as hds
import src.StoplossStrategy as sls
import src.StoplossType as slt
import datetime
import src.DatabaseConnector as dbc
from psycopg2 import sql
import logging

logging.basicConfig(level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(message)s',
      filename='./tmp/backtest.log',
      filemode='w')

class Results:

    def __init__(self, db_name: str, initial_assets):
        self._finalized = False
        self._db_name = db_name

        # CREATE new table in database to store the results (for each date, which tickers are held)
        dbConn = dbc.DatabaseConnector(self._db_name)
        dbConn.execute("DROP TABLE IF EXISTS results;", commit=True)
        dbConn.execute("DROP TABLE IF EXISTS final_raw;", commit=True)
        dbConn.execute("DROP TABLE IF EXISTS final_grouped;", commit=True)
        dbConn.execute("""CREATE TABLE results(
            date DATE NOT NULL,
            ticker VARCHAR(10) NOT NULL
            );""", commit=True)

    def add_result(self, result: hds.Holdings, current_date):
        """
        
        """
        if self._finalized == True:
            return -1
        
        # For each holding in the results object, create and add a new row to the results table
        for holding in result.get_holdings():
            dbConn = dbc.DatabaseConnector(self._db_name)
            query = sql.SQL("INSERT INTO results (date, ticker) VALUES (%s, %s);")
            dbConn.execute(query, commit=True, params=[current_date, holding.ticker_symbol])

    def finalize(self):
        """
            This function performs final database operations required
            to complete a backtest including credating tables to store
            backtest data.
        """
        # Lock result object so no more data can be written to it
        self._finalized = True

        # Create finalized_results table on JOIN of raw data and results
        logging.info("CREATING FINAL TABLE")
        dbConn = dbc.DatabaseConnector(self._db_name)

        # Create new table containing raw data from the backtest
        dbConn.execute("""CREATE TABLE final_raw AS (
            SELECT td.* FROM test_data td RIGHT JOIN results rs ON td.date = rs.date AND td.ticker = rs.ticker
        )""", commit=True)

        # Create a new table containing the backtest result data grouped by date
        dbConn.execute("""CREATE TABLE final_grouped AS (
            SELECT date, SUM(price) as price FROM final_raw GROUP BY date
            ORDER BY date
        )""", commit=True)