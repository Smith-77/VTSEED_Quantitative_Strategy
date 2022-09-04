from datetime import date
import pytest

import src.Holding as hd

@pytest.fixture()
def valid_holding():
    return hd.Holding('test_holding', 'nyse', date.today(), date.today(), 0.1, 0.1)

def test_get_ticker_symbol(valid_holding):
    assert valid_holding.ticker_symbol == "test_holding"