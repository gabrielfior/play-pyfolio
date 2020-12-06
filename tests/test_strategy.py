import pytest

from buy_hold_analyser.BuyHolder import Strategy


def test_strategy_init():
    with pytest.raises(AssertionError) as excinfo:
        # not allowed to have different lengths of assets and allocations
        s = Strategy(['VUSA'],[0.1,0.2])

def test_strategy_allocations():
    with pytest.raises(AssertionError) as excinfo:
        # not allowed to have allocations that do not sum to 1
        s = Strategy(['STOXX.DE','VUSA.DE'],[0.1,0.2])
