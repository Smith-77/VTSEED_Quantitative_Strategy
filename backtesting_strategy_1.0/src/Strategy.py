import src.Holdings as hds
import src.StoplossStrategy as sls
import src.StoplossType as slt
import src.Results as rs
import datetime
import src.DatabaseConnector as dbc

class Strategy:

    def __init__(self, max_holdings: int, days_between_rebalance: int, stoploss_type: slt.StoplossType = slt.StoplossType.NONE, trailing_days:int = None):
        self._holdings = hds.Holdings(max_holdings)
        self._days_between_rebalance = days_between_rebalance
        self._results = rs.Results()
        self._stoplossStrategy = sls.StoplossStrategy()
        if not self._stoplossStrategy.set_stoploss_type(stoploss_type, trailing_days):
            raise Exception("Error setting stoploss strategy. Ensure trailng_days is set to None if strategy type is NONE or ABSOLUTE and not None if TRAILING")
        
    def get_max_holdings(self):
        return self._holdings.get_max_holdings()

    def get_days_between_rebalance(self):
        return self._days_between_rebalance

    def get_stoplossStrategy(self):
        return self._stoplossStrategy

    def time_to_reevaluate(self, start_date, current_date) -> bool:
        time_difference = current_date - start_date
        days_elapsed = time_difference.days
        return (days_elapsed % self._days_between_rebalance) == 0

    #Complete as appropriate: ______________________________________________________

    def reevaluate_holdings(self, current_date: datetime.date) -> int: # Should uninverse pass???
        # assert self._holdings.get_current_holdings_number() == 0
        
        # implement as necessary
        
        # Temporary setup
        print("re-evaluating")
        dbConn = dbc.DatabaseConnector("./persistence/databases/test_data.db")
        print(current_date)
        rawResult = dbConn.execute("""
            SELECT Date, Ticker, Price FROM
                (SELECT * FROM time_data WHERE Date = ?)
            WHERE FCF_TTM > ? ORDER BY NET_INCOME_TTM DESC LIMIT %d
            """ % (self.get_max_holdings()), fetch='all', params=(current_date, 50)) # TODO: String substitution unsafe

        self._holdings.updateWithSQL(rawResult)
        self._results.add_result(self._holdings)

        return 1

        # results to holdings
        # Temporary Screener using pandas DF instead of database
        # return holdings


    def apply_stoplosses(self, current_date) -> int:
        curr_holdings = self._holdings
            

    def calculate_stoploss_percentage(ticker: str) -> float:
        # TODO
        pass

    def complete(self):
        self._results.finalize()
        return self._results
        # self._results.plot()