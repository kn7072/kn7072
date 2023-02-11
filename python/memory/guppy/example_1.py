# coding: utf-8
# https://coderzcolumn.com/tutorials/python/guppy-heapy-profile-memory-usage-in-python

"""
We'll first explain how to access heap status as a part of our first example and then will slowly build on it.

    guppy.hpy() - The guppy has method named hpy() which gives us access to heapy object. This will be the first method called by all our examples in order to get the heapy object which will provide a common interface for accessing heap status and performing other operations as well.

    heap() - This method is available through object created by calling hpy() method. This method provides a list of objects accessible from the root of the heap which are reachable and visible. The returned result is presented in a table format. Please make a note that it does not include objects used as a part of guppy.

    setref() - This method is available through heapy object created by calling hpy(). It is used to set a reference point and all objects created after this reference point will be available in the next call to the heap() method for heap status. It'll not include all objects present in heap but only once created after the reference point.

Below we have explained the usage of all these 3 methods. We have first collected heap status at the beginning of the script. We have then set the reference point and retrieved the heap status again. Then we have created a few objects like list, string, and numpy array of random numbers. After the creation of these objects, we have again called the heap() method to get heap status which has information about these objects.

We can see from the output that it has information about a number of objects and the total size of the whole heap as well as object count, size, % of memory used by that object type, and type information. The second heap status does not much info as not much has happened after setting up a reference point. The third heap status object has information about objects created after setting a reference point.
"""

from guppy import hpy
import numpy as np


def log_memory(log, heap, msg, percentage=50):
    first_line = "Total Objects: %s, Total Size: %s"
    log(msg)
    log(first_line % (heap.count, heap.size))
    log(f"Выводятся только объекты, суммарный размер который превышает {percentage}% от общего размера {heap.size}")
    stat = heap.stat if getattr(heap, "get_rows", None) is None else heap
    for row in stat.get_rows():
        if (row.cumulsize / heap.size) * 100 < percentage:
            log("%5d%5d%8d%8d%30s"%(row.index, row.count, row.size, row.cumulsize, row.name))
        else:
            break
    log(str(heap))


heap = hpy()

heap_status0 = heap.heap()
print("Heap Status At Starting : ")
heap_status1 = heap.heap()
print("Heap Size : ", heap_status1.size, " bytes\n")
print(heap_status1)

memory_diff = heap_status1.diff(heap_status0)
print("DIFF \n", str(memory_diff))

log_memory(print, heap_status0, "before")
log_memory(print, heap_status1, "after")
log_memory(print, memory_diff, "diff")

heap.setref()

print("\nHeap Status After Setting Reference Point : ")
heap_status2 = heap.heap()
print("Heap Size : ", heap_status2.size, " bytes\n")
print(heap_status2)

a = [i for i in range(1000)]
b = "A"
c = np.random.randint(1, 100, (1000,))

print("\nHeap Status After Creating Few Objects : ")
heap_status3 = heap.heap()
print("Heap Size : ", heap_status3.size, " bytes\n")
print(heap_status3)

print("\nMemory Usage After Creation Of Objects : ", heap_status3.size - heap_status2.size, " bytes")
