# coding:utf-8

from data_package import A
from guppy import hpy

from common import print_heap
import random

random.seed(1)


heap = hpy()
heap.setref()

count_instance = 1000
temp_list = [A(random.randint(0, 100000)) for _ in range(count_instance)]
temp_dict = {random.randint(0, 100000): i for i in range(count_instance)}
a = A(777)

dict_for_list = {random.randint(500, 10000): i for i in range(count_instance)}
list_with_dict = [1, 2, 3, 4, 5, dict_for_list]

print_heap(heap.heap().byvia)

"""
если нет словаря __dict__ в A

Partition of a set of 1242 objects. Total size = 69456 bytes.
 Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
     0   1001  81    48048  69     48048  69 data_package.module_a.A
"""

"""
Partition of a set of 3241 objects. Total size = 201504 bytes.
 Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
     0   1001  31   104104  52    104104  52 dict of data_package.module_a.A
     1   1001  31    48048  24    152152  76 data_package.module_a.A
"""

heap_a = heap.heap()
print_heap(heap_a)
print_heap(hpy().iso(a, a.__dict__, a.a, 1, 1, 1.0, [], [], temp_list, {"a": 1000}, {}))

for i in range(5):
    count_i = 10 ** i
    print(f"Количество элементов списка {count_i}")
    print_heap(hpy().iso([random.randint(500, 100000) for _ in range(count_i)]))

print("#" * 50 + "\n")
heap_b = heap.heap()
print_heap(heap_b)

print_heap(heap_b.bymodule)

print_heap(heap_b.byvia)