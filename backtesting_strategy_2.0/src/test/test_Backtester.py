from asyncio.windows_events import NULL
import pytest
import datetime

import src.Backtester as btst
import src.Strategy as str

@pytest.fixture()
def backtester():
    return btst.Backtester()

@pytest.fixture()
def strategy():
    return str.Strategy(10, 90)

def test_backtest(backtester, strategy):
    backtestID = backtester.backtest(strategy, datetime.date(2022, 1, 1), datetime.date(2022, 6, 1))
    assert backtestID >= 0

    # TODO
    # check that backtestID works with database, etc.