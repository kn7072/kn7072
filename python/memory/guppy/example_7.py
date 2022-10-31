# coding: utf-8
# https://coderzcolumn.com/tutorials/python/guppy-heapy-profile-memory-usage-in-python

"""
As a part of this example, we'll explain two useful methods available through the heap object.

    iso() - It takes as input single object or multiple objects and returns status specifying object size. 
        It considers complex objects like list, dict as one object.
    idset() - It takes as input single object or multiple objects and returns status specifying object size. 
        It considers complex objects like list, dict as a list of the individual object.

Please feel free to go through the below example to see the difference between the results of the two methods.
"""

from guppy import hpy


heap = hpy()

a = [i for i in range(1000000)]
b = "A"
c = "WORLD"


print("============== ISO Method Examples ====================")
print()
print(heap.iso(a))
print()
print(heap.iso(b))
print()
print(heap.iso(c))
print()
print(heap.iso([]))
print()
print(heap.iso(""))

print("\n============== IDSET Method Examples ===================")
print()
print(heap.idset(a))
print()
print(heap.idset(b))
print()
print(heap.idset(c))
print()
print(heap.idset([]))
print()
print(heap.idset(""))
