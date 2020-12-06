import pytest

from buy_hold_analyser import BuyHolder


def dummy_test():
    a = BuyHolder()
    assert a.dummy() == 1
