import src.Backtester as btst
import src.Strategy as str
import src.StoplossStrategy as sls
import src.StoplossType as slt
import datetime

# Create Strategy
stoplossStrategy = sls.StoplossStrategy(type=slt.StoplossType.ABSOLUTE, maxDrop=.0075, trailing_days=None)
strategy1 = str.Strategy(max_holdings=3, days_between_rebalance=2, stoplossStrategy=stoplossStrategy)
strategy2 = str.Strategy(max_holdings=4, days_between_rebalance=10, stoplossStrategy=stoplossStrategy)

# Create Backtester and backtest strategy
backtester = btst.Backtester(db_name='seed')
backtester.backtest(strategy1, datetime.date(2022, 1, 1), datetime.date(2022, 1, 21), table_name='test_data')
backtester.backtest(strategy2, datetime.date(2022, 1, 1), datetime.date(2022, 1, 21), table_name='test_data')