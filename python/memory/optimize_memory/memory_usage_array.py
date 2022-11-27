# -*- coding: utf-8 -*-

import array
from memory_profiler import memory_usage


# https://gist.github.com/MartinHeinz/3211bfc631275863feef33356a967394#file-memory_usage_array-py


def allocate(size):
    some_var = array.array('l', range(size))


usage = memory_usage((allocate, (int(1e7),)))
peak = max(usage)
print(f"Usage over time: {usage}")
# Usage over time: [39.71484375, 39.71484375, 55.34765625, 71.14453125, 86.54296875, 101.49609375, 39.73046875]
print(f"Peak usage: {peak}")
# Peak usage: 101.49609375
