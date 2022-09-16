import src.Holdings as hds
import src.StoplossStrategy as sls
import src.StoplossType as slt
import src.Results as rs
import datetime
import src.DatabaseConnector as dbc
from psycopg2 import sql

class Strategy:

    def __init__(self, max_holdings: int, days_between_rebalance: int, stoplossStrategy: sls.StoplossStrategy):
        self._holdings = hds.Holdings(max_holdings)
        self._days_between_rebalance = days_between_rebalance
        self._stoplossStrategy = stoplossStrategy
        self._db_name = None

    def initialize_db_name(self, db_name: str):
        self._db_name = db_name

    def get_days_between_rebalance(self):
        return self._days_between_rebalance

    def get_stoplossStrategy(self):
        return self._stoplossStrategy

    def time_to_rebalance(self, start_date, current_date) -> bool:
        time_difference = current_date - start_date
        days_elapsed = time_difference.days
        return (days_elapsed % self._days_between_rebalance) == 0

    #Complete as appropriate: ______________________________________________________

    def rebalance_holdings(self, current_date: datetime.date) -> int: # Should uninverse pass???
        print("\tRebalancing holdings...")

        # implement as necessary - temporary setup
        dbConn = dbc.DatabaseConnector(self._db_name)
        query = sql.SQL("""
                        SELECT Date, Ticker, Price 
                        FROM 
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
                            limit=sql.Literal(self._holdings.get_max_holdings())
                        )
        rawResult = dbConn.execute(query, fetch='all', params=[current_date, 50])

        '''
        rawResult = dbConn.execute("""
            SELECT Date, Ticker, Price FROM
                (SELECT * FROM test_data WHERE Date = %s)
            WHERE FCF_TTM > %s ORDER BY NET_INCOME_TTM DESC LIMIT %d
            """ % (self._holdings.get_max_holdings()), fetch='all', params=[current_date, 50]) # TODO: String substitution unsafe
        '''

        self._holdings.updateWithSQL(rawResult)
        return self._holdings

        # results to holdings
        # Temporary Screener using pandas DF instead of database
        # return holdings


    def apply_stoplosses(self, start_date, current_date) -> int:
        print("\tEvaluating for stoplosses...")

        stoploss_type = self._stoplossStrategy.get_stoploss_type()
        print(stoploss_type)
        dbConn = dbc.DatabaseConnector(self._db_name)

        if stoploss_type == slt.StoplossType.NONE:
            # print("NONE stoploss strategy")
            pass
        else: # TRAILING or ABSOLUTE Stoploss Strategy
            stoploss_date = start_date

            if stoploss_type == slt.StoplossType.TRAILING:
                # print("TRAILING stoploss strategy")
                stoploss_date = (start_date - datetime.timedelta(days=self._stoplossStrategy.get_trailing_days()))
            else:
                assert stoploss_type == slt.StoplossType.ABSOLUTE
                # print("ABSOLUTE stoploss strategy")

            # Iterate over all holdings. If holding has exceeded stoploss
            for current_holding in self._holdings.get_holdings():
                holding_ticker = current_holding.ticker_symbol

                # Ignore holding if it's already been converted to cash
                if current_holding.cash:
                    continue

                # Only evaluate stop loss if the comparison date is within the window of evaluation 
                if (stoploss_date - start_date).days >= 0:
                    query = sql.SQL("SELECT price FROM {table_name} WHERE DATE = %s AND Ticker = %s;").format(
                        table_name=sql.Identifier('test_data'))

                    initial_price = dbConn.execute(query, fetch="one", params=(stoploss_date, holding_ticker))[0]
                    current_price = dbConn.execute(query, fetch="one", params=(current_date, holding_ticker))[0]
                    percentChange = (current_price - initial_price) / initial_price
                    
                    # If the percent price change exceeds the specified limit, convert the holding to cash
                    if abs(percentChange) >= self._stoplossStrategy.get_max_drop(): # TODO: add as property
                        print("\t\tSelling %s due to stoploss" % (holding_ticker))
                        self._holdings.convert_holding_to_cash(holding_ticker, current_date)
            
        return self._holdings