from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime
import math
from typing import List

import backtrader as bt
import matplotlib
import pandas as pd
import pyfolio as pf
from backtrader.utils.py3 import iteritems

from buy_hold_analyser import BuyAndHoldStrategy
%matplotlib inline

def get_data_feed_by_name(data_feed_name, start, end):
    return bt.feeds.YahooFinanceData(dataname=data_feed_name,period='d', fromdate=start,
                                todate=end)

def get_local_data_feed_by_name(data_filename,start,end):
    return bt.feeds.YahooFinanceCSVData(
        dataname=data_filename,
        # Do not pass values before this date
        fromdate=start,
        # Do not pass values after this date
        todate=end,
        reverse=False)

class Strategy:
    def __init__(self, stocks: List, allocations: List):
        self.validate(stocks, allocations)

        self.execution_strategy = {k: v for k, v in zip(stocks, allocations)}

    def validate(self, stocks: List[str], allocations: List[float]):
        assert len(stocks) == len(allocations)
        assert math.isclose(1, sum(allocations), rel_tol=1e-3)

class BuyHolder():
    """ Class for executing transactions with given strategy. """

    def __init__(self, strategies: List[Strategy], start_analysis: datetime.datetime,
                 end_analysis: datetime.datetime):
        self.strategies = strategies
        self.start_analysis = start_analysis
        self.end_analysis = end_analysis


    def analyse(self):
        self.do_transactions()
        raise NotImplementedError()

    def do_transactions(self):
        data_vusa_csv = get_local_data_feed_by_name('VUSA.DE.csv', self.start_analysis, self.end_analysis)
        data_stoxx_csv = get_local_data_feed_by_name('EXSA.DE.csv', self.start_analysis, self.end_analysis)

        '''
        etf_allocation = {'vusa': (data_vusa, 0.5),
                          'stoxx': (data_stoxx, 0.5),
                          # 'emerging_markets':(data_emerging_markets,0.333),
                          # 'nasdaq100':(data_nasdaq100,0.333),
                          # 'china':(data_china,0.05),
                          # 'pacific':(data_pacific,0.05),'bonds':(data_bonds,0.1),
                          # 'japan':(data_japan,0.03), 'tech':(data_tech,0.02)
                          }
        '''

        etf_allocation_csv = {'vusa': (data_vusa_csv, 0.5),
                              'stoxx': (data_stoxx_csv, 0.5)
                              # 'nasdaq100':(data_nasdaq100_csv,0.25),'china':(data_china_csv,0.05),
                              # 'pacific':(data_pacific_csv,0.05),
                              # 'pacific':(data_pacific,0.05),
                              #     'bonds':(data_bonds_csv,0.05),
                              # 'japan':(data_japan_csv,0.05), 'tech':(data_tech_csv,0.05)
                              }


        cerebro = bt.Cerebro()

        # Add a strategy
        cerebro.addstrategy(BuyAndHoldStrategy)
        cerebro.broker.set_cash(0.000001)
        cerebro.broker.set_fundmode(True)

        for data_name, (data_feed, percent_allocation) in etf_allocation_csv.items():
            cerebro.adddata(data_feed, name=data_name)

        print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

        cerebro.addobserver(bt.observers.TimeReturn, timeframe=bt.TimeFrame.Days)

        # Analyzers
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio', timeframe=bt.TimeFrame.Days)
        cerebro.addanalyzer(bt.analyzers.PositionsValue, headers=True, cash=True, _name='mypositions')
        cerebro.addanalyzer(bt.analyzers.TimeReturn, _name='timereturn')

        results = cerebro.run()

        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
        return results

    def display_results(self, results):
        strat = results[0]
        pyfoliozer = strat.analyzers.getbyname('pyfolio', )
        returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()  # <--positions only holds data for one symbol here

        p = strat.analyzers.getbyname('mypositions').get_analysis()
        mypositions = [[k] + v for k, v in iteritems(p)]  # <-- Now positions will hold data for all symbols
        cols = mypositions.pop(0)  # headers are in the first entry
        mypositions = pd.DataFrame.from_records(mypositions, index=cols[0], columns=cols)
        mypositions.index = pd.DatetimeIndex(mypositions.index)

        strat = results[0]
        timereturn_analyzer = strat.analyzers.getbyname('timereturn')
        timereturn = timereturn_analyzer.get_analysis()

        timereturn_df = pd.DataFrame([(k, v) for k, v in timereturn.items()], columns=['date', 'return'])
        timereturn_df.set_index('date', inplace=True)

        # ToDo - Plot only figure
        pf.create_interesting_times_tear_sheet(timereturn_df['return'])
