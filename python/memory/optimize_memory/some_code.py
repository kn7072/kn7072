# -*- coding: utf-8 -*-

# https://github.com/pythonprofilers/memory_profiler
# pip install memory_profiler psutil
# psutil is needed for better memory_profiler performance

# python3 -m memory_profiler some_code.py


from memory_profiler import profile


fp = open('memory_profiler.log','w+')


@profile(stream=fp)
def memory_intensive():
    small_list = [None] * 1000000
    big_list = [None] * 10000000
    del big_list
    return small_list


memory_intensive()
