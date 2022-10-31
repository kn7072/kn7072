# coding: utf-8

# https://coderzcolumn.com/tutorials/python/guppy-heapy-profile-memory-usage-in-python

"""
Example 2

As a part of the second example, we'll explain how to access objects which are not reachable from the root of the heap. This is generally created using cycle references.

    heapu() - This method is available through an object created by calling hpy() method of guppy module. 
        This method provides us heap status about the list of objects which are not reachable from the root of the heap. 
        The object returned by heapu() method is a status object (guppy.heapy.Part.Stat) which has stats about unreachable objects.

Below we have first retrieved a list of unreachable objects from the heap and then used various methods to access an individual row of status to retrieve information about the individual data type.

If you are interested in learning about memory management in python then please feel free to check our tutorial on the same.
"""

from guppy import hpy


heap = hpy()

print("GC Collectable Objects Which Are not Reachable from Root of Heap")

stats = heap.heapu()

print("Total Objects : ", stats.count)
print("Total Size : ", stats.size, " Bytes")
print("Number of Entries : ", stats.numrows)

print("Entries : ")

print("Index Count  Size  Cumulative Size         Object Name")
for row in stats.get_rows():
    print("%5d%5d%8d%8d%30s" % (row.index, row.count, row.size, row.cumulsize, row.name))


print("\nFirst 5 Entries : ")
print("Index Count  Size  Cumulative Size         Object Name")
for row in stats.rows[:5]:
    print("%5d%5d%8d%8d%30s" % (row.index, row.count, row.size, row.cumulsize, row.name))

print("\nDirectly Printing Results Without Iteration")
print(heap.heapu(stat=0))

print("\nMeasuring Unreachable Objects From This Reference Point Onwards")
heap.setref()
print(heap.heapu(stat=0))
