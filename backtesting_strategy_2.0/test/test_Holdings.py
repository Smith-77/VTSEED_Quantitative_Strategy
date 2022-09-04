from datetime import date
import pytest

import src.Holding as hd
import src.Holdings as hds

@pytest.fixture()
def valid_holding():
    holdings = []
    holdings.append(hd.Holding('test_holding1', 'nyse', date.today(), date.today(), 0.1, 0.1))
    holdings.append(hd.Holding('test_holding2', 'nyse', date.today(), date.today(), 0.1, 0.1))
    holdings.append(hd.Holding('test_holding3', 'nyse', date.today(), date.today(), 0.1, 0.1))
    holdings.append(hd.Holding('test_holding4', 'nyse', date.today(), date.today(), 0.1, 0.1))
    return holdings

@pytest.fixture()
def valid_holdings():
    return hds.Holdings(3)

def test_add_holding(valid_holding, valid_holdings):
    assert valid_holdings.add_holding(valid_holding[0]) # holding successfully added
    assert not valid_holdings.add_holding(valid_holding[0]) # ticker already present
    assert not valid_holdings.add_holding("valid_holding") # holding not a Holding class
    assert valid_holdings.add_holding(valid_holding[1])
    assert valid_holdings.add_holding(valid_holding[2])
    assert not valid_holdings.add_holding(valid_holding[3]) # Max holdings exceeded

def test_remove_holding(valid_holding, valid_holdings):
    valid_holdings.add_holding(valid_holding[0])
    valid_holdings.add_holding(valid_holding[1])
    valid_holdings.add_holding(valid_holding[2])
    assert valid_holdings.remove_holding(valid_holding[0].ticker_symbol) # ticker successfully removed
    assert not valid_holdings.remove_holding(valid_holding[0].ticker_symbol) # ticker not present
    assert not valid_holdings.remove_holding(valid_holding[0]) # holding ticker isn't a string
    assert valid_holdings.remove_holding(valid_holding[1].ticker_symbol)
    assert valid_holdings.remove_holding(valid_holding[2].ticker_symbol)

def test_get_max_holdings(valid_holdings):
    assert valid_holdings.get_max_holdings() == 3

def test_get_current_holdings_number(valid_holdings, valid_holding):
    assert valid_holdings.get_current_holdings_number() == 0
    valid_holdings.add_holding(valid_holding[0])
    assert valid_holdings.get_current_holdings_number() == 1
    valid_holdings.remove_holding(valid_holding[0].ticker_symbol)
    assert valid_holdings.get_current_holdings_number() == 0

def test_ticker_in_holdings(valid_holdings, valid_holding):
    assert not valid_holdings.ticker_in_holdings("test_holding1")
    valid_holdings.add_holding(valid_holding[0])
    assert valid_holdings.ticker_in_holdings("test_holding1")
    assert not valid_holdings.ticker_in_holdings("test_holding3")

def test_get_holdings_tickers(valid_holdings, valid_holding):
    assert valid_holdings.get_holdings_tickers() == set({})
    valid_holdings.add_holding(valid_holding[0])
    assert valid_holdings.get_holdings_tickers() == {"test_holding1"}
    valid_holdings.add_holding(valid_holding[1])
    valid_holdings.add_holding(valid_holding[2])
    assert valid_holdings.get_holdings_tickers() == {"test_holding1", "test_holding2", "test_holding3"}