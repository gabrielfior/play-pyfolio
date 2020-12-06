import datetime

from buy_hold_analyser.BuyHolder import BuyHolder


def test_ops(dummy_from_conftest):
    assert dummy_from_conftest is not None

def test_dummy():
    a = BuyHolder([],datetime.datetime.today(),datetime.datetime.today())
    assert a is not None

def test_buy_hold_analyse():

