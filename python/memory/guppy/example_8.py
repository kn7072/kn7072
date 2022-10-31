# coding: utf-8
# https://coderzcolumn.com/tutorials/python/guppy-heapy-profile-memory-usage-in-python

"""
Example 8

As a part of our eighth and last example, we have demonstrated how we can check doc of particular method/attributes of objects available through guppy.

Below we have accessed the document of the heap by calling the doc attribute of a heap object. 
It'll show documentation for the whole heap object listing all methods/attributes available through that object. 
We have also accessed the document of individual method/attribute by calling that method attributes name on the doc attribute as explained below.

We have also accessed documentation of the heap status object. Please feel free to go through the below example 
to check how we can access docs of guppy objects.
"""

from guppy import hpy

heap = hpy()

heap_status1 = heap.heap()

print("============== Heap Documents ====================")
print(heap.doc)

print("Doc On Individual Method/Function/Class : ")
print("\nISO Method Doc : \n")
print(heap.doc.iso)

print("\nRoot Class Doc : \n")
print(heap.doc.Root)


print("============= Heap Status Documents ================")
print(heap_status1.doc)

print("Doc On Individual Method/Function/Class : ")

print("\nDoc on parts Property of Heap Status : \n")
print(heap_status1.doc.parts)
print("\nDoc on byrcs Property of Heap Status : \n")
print(heap_status1.doc.byrcs)
