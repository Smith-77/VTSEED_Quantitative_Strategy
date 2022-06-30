import src.Backtester as btst
import src.Strategy as str
import src.StoplossType as slt
import datetime

# Create Strategy
strategy1 = str.Strategy(10, 90, slt.StoplossType.NONE, None)

# Create Backtester and backtest strategy
backtester = btst.Backtester()
backtestID = backtester.backtest(strategy1, datetime.date(2022, 1, 1), datetime.date(2022, 7, 1))

# Visualize the backtest
# visualizer = vs.Visualizer(backtestID)
# visualizer.plot()