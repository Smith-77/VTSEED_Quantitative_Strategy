import pytest

import src.Strategy as strat
import src.StoplossStrategy as sls
import datetime

@pytest.fixture()
def strategy():
    return strat.Strategy(10, 90, sls.StoplossStrategy())

def test_time_to_reevaluate_true(strategy):
    start_date = datetime.date(2022, 1, 1)
    current_date = start_date + datetime.timedelta(days = 90)
    assert strategy.reevaluate(start_date, current_date)
    current_date = start_date + datetime.timedelta(days = 0)
    assert strategy.reevaluate(start_date, current_date)

def test_time_to_reevaluate_false(strategy):
    start_date = datetime.date(2022, 1, 1)
    current_date = start_date + datetime.timedelta(days = 89)
    assert not strategy.reevaluate(start_date, current_date)