# coding: utf-8
# https://coderzcolumn.com/tutorials/python/guppy-heapy-profile-memory-usage-in-python

"""
Example 6

As a part of the sixth example, we have explained various attributes available through heap status object which lets us group heap status 
entries based on different attributes like, type, size, referrers, memory address, etc.

    bytype - This attribute of heap status groups heap status entries by type of object. All dict entries will be combined into one entry.
    byrcs - This attribute of heap status groups heap status entries by type of referrers.
    bymodule - This attribute of heap status groups heap status entries by the module.
    bysize - This attribute of heap status groups heap status entries by the individual size of object.
    byunity - This attribute of heap status groups heap status entries by total size.
    byvia -This attribute of heap status groups heap status entries by objects via which they are referred.
    byidset - This attribute of heap status groups heap status entries by idset.
    byid - This attribute of heap status groups heap status entries by memory address.

Below we have explained all attributes mentioned above one by one. We can easily see results to see how objects are grouped by.
"""

from guppy import hpy

heap = hpy()
heap_status1 = heap.heap()

print("=========== Heap Status At Starting : ============")
print(heap_status1)

print("\n============ Heap Status Grouped By Type : ==========")
print(heap_status1.bytype)

print("\n==== Heap Status Grouped By Referrers of kind(class/dict of class) : ===")
print(heap_status1.byrcs)

print("\n========== Heap Status Grouped By Module : ============")
print(heap_status1.bymodule)

print("\n========== Heap Status Grouped By Individual Size : ==============")
print(heap_status1.bysize)

print("\n========= Heap Status Grouped By Total Size : ============")
print(heap_status1.byunity)

print("\n======= Heap Status Grouped By Referred Via : =============")
print(heap_status1.byvia)

print("\n========= Heap Status Grouped By IDset : ============")
print(heap_status1.byidset)

print("\n======== Heap Status Grouped By Address : ==========")
print(heap_status1.byid)
