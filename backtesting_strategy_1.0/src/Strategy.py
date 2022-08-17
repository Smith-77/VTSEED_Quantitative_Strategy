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
        dbConn = dbc.DatabaseConnector("./persistence/databases/test_data.db")
        rawResult = dbConn.execute("""
            SELECT Date, Ticker, Price FROM
                (SELECT * FROM time_data WHERE Date = ?)
            WHERE FCF_TTM > ? ORDER BY NET_INCOME_TTM DESC LIMIT %d
            """ % (self._holdings.get_max_holdings()), fetch='all', params=(current_date, 50)) # TODO: String substitution unsafe

        self._holdings.updateWithSQL(rawResult)
        self._results.add_result(self._holdings, current_date)

        return 1

        # results to holdings
        # Temporary Screener using pandas DF instead of database
        # return holdings


    def apply_stoplosses(self, start_date, current_date) -> int:
        print("\tEvaluating for stoplosses...")

        stoploss_type = self._stoplossStrategy.get_stoploss_type()
        dbConn = dbc.DatabaseConnector("./persistence/databases/test_data.db")

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
                    initial_price = dbConn.execute("""
                                                SELECT price FROM time_data WHERE DATE = ? AND Ticker = ?;
                                                """, fetch="one", params=(stoploss_date, holding_ticker))[0]
                    current_price = dbConn.execute("""
                                                SELECT price FROM time_data WHERE DATE = ? AND Ticker = ?;
                                                """, fetch="one", params=(current_date, holding_ticker))[0]
                    percentChange = (current_price - initial_price) / initial_price
                    
                    # If the percent price change exceeds the specified limit, convert the holding to cash
                    if percentChange <= -0.0075: # TODO: add as property
                        print("\t\tSelling %s due to stoploss" % (holding_ticker))
                        self._holdings.convert_holding_to_cash(holding_ticker, current_date)
            
        self._results.add_result(self._holdings, current_date)
            

    def calculate_stoploss_percentage(ticker: str) -> float:
        # TODO
        pass

    def complete(self):
        self._results.finalize()
        return self._results
        # self._results.plot()