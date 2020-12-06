# play_pyfolio

This repository aims at comparing different allocations within the Buy-and-Hold overarching strategy.

## Getting started

```python
import buy_hold_analyser as bha
great_strategy = bha.Strategy()
another_great_strategy = bha.RandomStrategy()

executor = bha.BuyHolder([great_strategy, another_great_strategy])
executor.analyse()
executor.display_resulsts()
```
