# coding: utf-8
# https://coderzcolumn.com/tutorials/python/guppy-heapy-profile-memory-usage-in-python

"""
Example 4

As a part of our fourth example, we'll explain how we can find out the difference between two heap status to check how many objects 
were created between two calls of heap status.

    diff() - This method is available as a part of the heap status object which takes as input another heap status 
        to find out objects difference between two statuses. It returns an object of type guppy.heapy.Part.Stat which 
        we have explored as a part of our second example.

    disjoint() - This method is available through a heap status object that takes input another heap status and 
        returns True/False based on whether two heap status is disjoint or not.

Below we have first taken heap status at the beginning. We have then created a few lists of objects and string object. 
After the creation of these objects, we have again taken another heap status. We have then called the diff() method 
on the second heap status object passing it first heap status object to get the difference between two screenshots of the heap. 
We have then looped through stats object and printed the difference of objects.
"""

from guppy import hpy
import numpy as np


heap = hpy()

print("Heap Status At Starting : ")
heap_status1 = heap.heap()
print("Heap Size : ", heap_status1.size, " bytes\n")
print(heap_status1)


a = [i for i in range(1000)]
b = "A"
c = np.random.randint(1, 100, (1000,))

print("\nHeap Status After Creating Few Objects : ")
heap_status2 = heap.heap()
print("Heap Size : ", heap_status2.size, " bytes\n")
print(heap_status2)

print("\nMemory Usage After Creation Of Objects : ", heap_status2.size - heap_status1.size, " bytes")

print("\nFinding Out Difference Between Two Heap Status : ")
stats = heap_status2.diff(heap_status1)

print("Whether Two Heap Status Are Disjoint : ", heap_status1.disjoint(heap_status2))
print("Total Objects : ", stats.count)
print("Total Size : ", stats.size, " Bytes")
print("Number of Entries : ", stats.numrows)

print("Entries : ")

print("Index Count  Size  Cumulative Size         Object Name")
for row in stats.get_rows():
    print("%5d%5d%8d%8d%30s" % (row.index, row.count, row.size, row.cumulsize, row.name))
