import src.Holdings as hds
import src.StoplossStrategy as sls
import src.StoplossType as slt
import datetime
import src.DatabaseConnector as dbc
import pandas as pd

class Results:

    def __init__(self):
        self._rawDF = pd.DataFrame(columns=['Date','Ticker','Exchange','Date_First_Bought','Repeat','Multiplier','Price'])
        self._summaryDF = pd.DataFrame(columns=['Date','Tickers','Total_Price'])
        self._finalized = False

    def add_result(self, result: hds.Holdings):
        # Ensure results object can still be modified
        if self._finalized == True:
            return -1
        
        # For each holding in the results object, create and add a new row to the rawDF
        for holding in result.get_holdings():
            new_row = [holding.date_bought, holding.ticker_symbol, holding.exchange_symbol, holding.date_first_bought, holding.repeat, holding.multiplier, holding.price]
            print(new_row[0], "################################")
            self._rawDF.loc[self._rawDF.shape[0]]= new_row

        print(self._rawDF.head(100))

        # dbConn = dbc.DatabaseConnector()
        # dbConn.execute("DROP TABLE IF EXISTS results_table") # TODO update for unique name
        # dbConn.execute("""CREATE TABLE results_table
        #                     (
        #                         Date datetime,
        #                         Tick
        #                     );""")

    def finalize(self):
        # Lock result object so no more data can be written to it
        print(self._rawDF.head(500))
        self._finalized = True

        # Generate _summaryDF
        # Generate Date list
        grouped_by_date_DF = self._rawDF.groupby('Date', as_index=False)
        dates = grouped_by_date_DF.sum()['Date']
        print(dates)
        print(type(dates))
        # Generate Total Price by Date
        prices = grouped_by_date_DF.sum()['Price']
        print(prices)
        print(type(prices))
        # Generate % Repeats by Date
        # repeat_percentages = self._rawDF.groupby('Date', as_index= False).
        # Compile Summary DF
        self._summaryDF = pd.DataFrame(columns=['Date', 'Price'])
        self._summaryDF['Date'] = dates
        self._summaryDF['Price'] = prices
        print(self._summaryDF.head(500))
        # self._summaryDF = self._rawDF.groupby(["Date"]).mean()
        # print(self._summaryDF['Price'])
        # print(type(self._summaryDF))
        # print(self._rawDF.groupby('Date')['Date'])
        # price = self._rawDF.groupby('Date').mean()['Price']
        # print(price)
        # self._summaryDF['Date'] = date
        # self._summaryDF['Price'] = price

    def plot(self):
        self._summaryDF.plot('Date', 'Price')

    def get_summary(self):
        return self.__summaryDF

    def result_to_sql(self):
        pass
