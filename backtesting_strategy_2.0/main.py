import src.Backtester as btst
import src.Strategy as str
import src.StoplossStrategy as sls
import src.StoplossType as slt
import datetime

# Create Strategy
stoplossStrategy = sls.StoplossStrategy(type=slt.StoplossType.ABSOLUTE, maxDrop=.0075, trailing_days=None)
strategy1 = str.Strategy(max_holdings=3, days_between_rebalance=2, stoplossStrategy=stoplossStrategy)

# Create Backtester and backtest strategy
backtester = btst.Backtester(db_name='seed', table_name='test_data')
resultsDF = backtester.backtest(strategy1, datetime.date(2022, 1, 1), datetime.date(2022, 1, 21))