# coding: utf-8
# https://coderzcolumn.com/tutorials/python/guppy-heapy-profile-memory-usage-in-python

"""
Example 5

As a part of this example, we'll explore a few methods available through heap status methods and attributes.

    count - This attribute of heap status object returns an integer specifying a total number of objects present when the status was taken.
    size - This attribute of heap status object returns an integer specifying the total size of the heap when the status was taken.
    referents - This attribute returns another heap status object with only entry for objects which are referred to by other objects.
    referrers - This attribute returns another heap status object with only entry for objects which are referring to other objects.
    stat - It returns guppy.heapy.Part.Stat which can be looped to get information about the individual entry of the heap status 
        as we had explained in our previous examples.
    dump() - It takes as input filename to which heap status will be dumped.
    load() - It takes as input filename from which heap status will be loaded. This method can be called over the object created by 
        calling the hpy() method. It returns guppy.heapy.Part.Stat object of heap status present in the file.

"""

from guppy import hpy


heap = hpy()

heap_status0 = heap.heap()
heap_status1 = heap.heap()


diff_heap = heap_status1.diff(heap_status0)
print(diff_heap.count)

print("\nFew Important Properties/Methods of Heap Status Object(%s) : " % type(heap_status1))

print("\nCount of Objects in Heap : ", heap_status1.count)
print("\nHeap Size : ", heap_status1.size, " bytes")
print("\nHeap 1st Entry : ")
print(heap_status1.parts[0])

print("\nSet of Objects Referred to By Any Objects : \n")
print(heap_status1.referents)

print("\nSet of Objects Directly Refer to Any Objects : \n")
print(heap_status1.referrers)

print("\nStat Object : ")
print(heap_status1.stat)
print("First 3 Entries : ")
print("Index Count  Size  Cumulative Size         Object Name")
for row in list(heap_status1.stat.get_rows())[:3]:
    print("%5d%5d%8d%8d%30s" % (row.index, row.count, row.size, row.cumulsize, row.name))


print("\nDumping Heap Status to a File : ")
heap_status1.dump("guppy_heap_status.out")
print(open("guppy_heap_status.out").readlines()[:5])

loaded_heap_stat = heap.load("guppy_heap_status.out")

print("First 3 Entries From Loaded File : ")
print("Index Count  Size  Cumulative Size         Object Name")
for row in list(loaded_heap_stat.get_rows())[:3]:
    print("%5d%5d%8d%8d%30s" % (row.index, row.count, row.size, row.cumulsize, row.name))
