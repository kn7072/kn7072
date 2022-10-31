# coding: utf-8

# https://coderzcolumn.com/tutorials/python/guppy-heapy-profile-memory-usage-in-python

"""
Example 3

As a part of this example, we'll explain how we can retrieve an individual entry from the whole heap status object.

Below we have retrieved heap status after creating few lists. The individual object can also be accessed 
from the heap status object by simply using list indexing. Below we have printed various individual entry of heap status. 
We have also created a simple method that takes as input size in bytes and returns size in KB/MB/GB.
"""

from guppy import hpy
import numpy as np


heap = hpy()

print("Heap Status At Starting : ")

l1 = [i*i for i in range(1000)]
l2 = np.random.randint(1, 100, (1000, 1000))

heap_status1 = heap.heap()

print(heap_status1)

print("\nAccessing Individual Element of Heap")

print("\nFirst Element : ")
print(heap_status1[0])

print("\nSecond Element : ")
print(heap_status1[1])

print("\nThird Element : ")
print(heap_status1.parts[2])


def convert_size(size):
    if size < 1024:
        return size
    elif (size >= 1024) and (size < (1024 * 1024)):
        return "%.2f KB" % (size/1024)
    elif (size >= (1024*1024)) and (size < (1024*1024*1024)):
        return "%.2f MB" % (size/(1024*1024))
    else:
        return "%.2f GB" % (size/(1024*1024*1024))


print("\nTotal Heap Size : ", convert_size(heap_status1.size), "\n")
for i in range(10):
    print("Size Of Object : %d - " % i, convert_size(heap_status1[i].size))
