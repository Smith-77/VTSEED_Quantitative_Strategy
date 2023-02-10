import src.Holdings as hds
import src.StoplossStrategy as sls
import src.StoplossType as slt
import src.Results as rs
import datetime
import src.DatabaseConnector as dbc
from psycopg2 import sql
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(message)s',
      filename='./tmp/backtest.log',
      filemode='w')

class Strategy:

    def __init__(self, max_holdings: int, days_between_rebalance: int, stoplossStrategy: sls.StoplossStrategy):
        self._max_holdings = max_holdings
        self._days_between_rebalance = days_between_rebalance
        self._stoplossStrategy = stoplossStrategy
        self._db_name = None
        self._table_name = None

    def set_db_name(self, db_name: str):
        self._db_name = db_name
        
    def set_table_name(self, table_name: str):
        self._table_name = table_name

    def get_days_between_rebalance(self):
        return self._days_between_rebalance

    def get_stoplossStrategy(self):
        return self._stoplossStrategy

    def get_max_holdings(self):
        return self._max_holdings

    def time_to_rebalance(self, start_date, current_date) -> bool:
        time_difference = current_date - start_date
        days_elapsed = time_difference.days
        return (days_elapsed % self._days_between_rebalance) == 0

    #Complete as appropriate: ______________________________________________________

    def rebalance_holdings(self, holdings: hds.Holdings, current_date: datetime.date) -> int: # Should uninverse pass???
        logging.info("\tRebalancing holdings...")

        # implement as necessary - temporary setup
        dbConn = dbc.DatabaseConnector(self._db_name)
        query = sql.SQL("""
                        SELECT Date, Ticker, Price FROM 
                        (
                            SELECT * FROM 
                            {table_name}
                            WHERE Date = %s
                        ) as layer1 
                        WHERE FCF_TTM > %s
                        ORDER BY NET_INCOME_TTM DESC 
                        LIMIT {limit}
                        """
                        ).format(
                            table_name=sql.Identifier('test_data'),
                            limit=sql.Literal(holdings.get_max_holdings())
                        )
        rawResult = dbConn.execute(query, fetch='all', params=[current_date, 50])

        ''' # This can be deleted later, I'm just keeping it as a reference for now
        rawResult = dbConn.execute("""
            SELECT Date, Ticker, Price FROM
                (SELECT * FROM test_data WHERE Date = %s)
            WHERE FCF_TTM > %s ORDER BY NET_INCOME_TTM DESC LIMIT %d
            """ % (self._holdings.get_max_holdings()), fetch='all', params=[current_date, 50]) # TODO: String substitution unsafe
        '''

        return self._update_holdings_with_sql_raw_result(holdings, rawResult)

        # results to holdings
        # Temporary Screener using pandas DF instead of database
        # return holdings

    def _update_holdings_with_sql_raw_result(self, holdings, rawResult):
        
        holdings.updateWithSQL(rawResult)
        return holdings

    def apply_stoplosses(self, holdings, start_date, current_date) -> int:
        logging.info("\tEvaluating for stoplosses...")

        stoploss_type = self._stoplossStrategy.get_stoploss_type()

        if stoploss_type == slt.StoplossType.ABSOLUTE:
            self._apply_absolute_stoplosses(holdings, start_date, current_date)
        elif stoploss_type == slt.StoplossType.TRAILING:
            self._apply_trailing_stoplosses(holdings, start_date, current_date)
        else:
            assert stoploss_type == slt.StoplossType.NONE

        return holdings

    def _apply_absolute_stoplosses(self, holdings, start_date, current_date):
        dbConn = dbc.DatabaseConnector(self._db_name)
        
        for holding in holdings.get_holdings():
            days_elapsed = (current_date - start_date).days

            # Holding shouldn't already be sold and date should be within valid time window
            if not holding.cash and days_elapsed >= 0:

                # Calculate percent change of price
                query = sql.SQL("SELECT price FROM {table_name} WHERE DATE = %s AND Ticker = %s;").format(
                    table_name=sql.Identifier('test_data'))

                initial_price = dbConn.execute(query, fetch="one", params=(start_date, holding.ticker_symbol))[0]
                current_price = dbConn.execute(query, fetch="one", params=(current_date, holding.ticker_symbol))[0]
                percentChange = (current_price - initial_price) / initial_price
                    
                # If the percent price change exceeds the specified limit, convert the holding to cash
                if abs(percentChange) >= self._stoplossStrategy.get_max_drop(): # TODO: add as property
                    logging.info("\t\tSelling %s due to stoploss" % (holding.ticker_symbol))
                    holdings.sell_holding_by_ticker(holding.ticker_symbol, current_date)

    def _apply_trailing_stoplosses(self, holdings, start_date, current_date):
        trailing_date = (current_date - datetime.timedelta(days=self._stoplossStrategy.get_trailing_days()))
        return self._apply_absolute_stoplosses(holdings, max(start_date, trailing_date), current_date)