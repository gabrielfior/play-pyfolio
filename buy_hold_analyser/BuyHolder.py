import datetime
from typing import List


class Strategy:
    def __init__(self, stocks: List, allocations: List):
        assert len(stocks) == len(allocations)
        self.execution_strategy = {k:v for k,v in zip(stocks, allocations)}

class BuyHolder():
    """ Class for executing transactions with given strategy. """
    def __init__(self, strategy: Strategy, start_analysis: datetime.datetime):
        self.strategy = strategy
        self.start_analysis = start
    
    def dummy(self):
        return 1

