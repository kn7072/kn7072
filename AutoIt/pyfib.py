import ctypes
import timeit

fib = ctypes.CDLL('./myfib.so').fib
fib.restype = ctypes.c_long
fib.argtypes = (ctypes.c_ulong,)

print (timeit.timeit('fib(32)', 'from __main__ import fib', number=1))

def pyfib(x):
    if x < 2: return x
    return pyfib(x-1) + pyfib(x-2)

print(timeit.timeit('pyfib(32)', 'from __main__ import pyfib', number=1))
print()
