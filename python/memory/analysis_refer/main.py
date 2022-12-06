# -*- coding: utf-8 -*-
import gc
import sys

from package.module_a import A1

a1 = A1()
# print()
# dict_all_link = A1.dict_ref
obj = A1.dict_ref["package.module_c.C"][0]()
# print(sys.getrefcount(obj))
print(gc.get_referents(obj))  # на что ссылается obj

for i in gc.get_referrers(obj):
    print(i)

print()
