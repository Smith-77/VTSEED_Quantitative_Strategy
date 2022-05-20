import pytest

import src.StoplossStrategy as sls
import src.StoplossType as slt

@pytest.fixture()
def stoploss():
    return sls.StoplossStrategy()

def test_set_no_stoploss(stoploss):
    assert stoploss.set_stoploss_type(slt.StoplossType.NONE)
    assert stoploss.get_trailing_days() == None
    assert stoploss.get_stoploss_type() == slt.StoplossType.NONE
    assert not stoploss.set_stoploss_type(slt.StoplossType.NONE, 1)

def test_set_absolute_stoploss(stoploss):
    assert stoploss.set_stoploss_type(slt.StoplossType.ABSOLUTE)
    assert stoploss.get_trailing_days() == None
    assert stoploss.get_stoploss_type() == slt.StoplossType.ABSOLUTE
    assert not stoploss.set_stoploss_type(slt.StoplossType.ABSOLUTE, 1)

def test_set_trailing_stoploss(stoploss):
    assert stoploss.set_stoploss_type(slt.StoplossType.TRAILING, 5)
    assert stoploss.get_trailing_days() == 5
    assert stoploss.get_stoploss_type() == slt.StoplossType.TRAILING
    assert not stoploss.set_stoploss_type(slt.StoplossType.TRAILING)
    assert not stoploss.set_stoploss_type(slt.StoplossType.TRAILING, "1")
    assert not stoploss.set_stoploss_type(slt.StoplossType.TRAILING, -1)

def test_get_trailing_days(stoploss):
    assert stoploss.get_trailing_days() == None

def test_get_stoploss_type(stoploss):
    assert stoploss.get_stoploss_type() == slt.StoplossType.NONE