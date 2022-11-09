# -*- coding: utf-8 -*-

# https://pymotw.com/3/gc/

import gc
import random
import sys


class B:
    pass


class A:
    def __init__(self):
        self.a = 100500
        self.b = B()

    def test(self):
        pass

# gc.collect()

a = A()
print(gc.get_debug())
print(f"BEFORE {len(gc.get_objects())}")
len_list = 1000
obj_list = [random.randint(500, 1000000) for _ in range(len_list)]
print(f"AFTER  {len(gc.get_objects())}")

ref_obj_list = gc.get_referrers(obj_list)  # вернет объекты ссылающиеся на obj_list
# ref_obj_list[0]["len_list"]

referrers_a_a = gc.get_referrers(a.a)
print(len(referrers_a_a))
print(referrers_a_a[0])

referrers_a_b = gc.get_referrers(a.b)
print(len(referrers_a_b))
print(referrers_a_b[0])

referrers_a_dict__a = gc.get_referrers(a.__dict__["a"])
print(len(referrers_a_dict__a))
print(referrers_a_dict__a[0])


referrers_a_test = gc.get_referrers(a.test)
print(len(referrers_a_test))
# print(referrers_a_test[0])

referrers_a_test = gc.get_referrers(A.test)
print(len(referrers_a_test))
print(referrers_a_test[0])

print("#"*20 + "\n")
print("referrers_a_dict__")
referrers_a_dict__ = gc.get_referrers(a.__dict__)
print(len(referrers_a_dict__))
print(referrers_a_dict__[0])

print("#"*20 + "\n")
print("referents_a")
referents_a = gc.get_referents(a)  # на какие объекты ссылается a
for r in gc.get_referents(referents_a):
    print(r)

print("#"*20 + "\n")
print("referents_a_dict__")
for r in gc.get_referents(a.__dict__):
    print(r)

print(sys.getrefcount(obj_list))