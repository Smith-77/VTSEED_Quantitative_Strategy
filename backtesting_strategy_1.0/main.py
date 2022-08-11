import src.Backtester as btst
import src.Strategy as str
import src.StoplossType as slt
import datetime
import src.DatabaseConnector as dbc
import os

# Set up the test database
# os.system("/src/persistence/createTestDB.py")

# Create Strategy
strategy1 = str.Strategy(1, 5, slt.StoplossType.NONE, None)

dbConn = dbc.DatabaseConnector("./persistence/databases/test_data.db")
print(dbConn.execute("SELECT date FROM time_data", fetch="one"))

# Create Backtester and backtest strategy
backtester = btst.Backtester()
backtestID = backtester.backtest(strategy1, datetime.date(2022, 1, 1), datetime.date(2022, 1, 20))

# Visualize the backtest
# visualizer = vs.Visualizer(backtestID)
# visualizer.plot()