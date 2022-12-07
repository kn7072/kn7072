# -*- coding: utf-8 -*-
import gc
import sys
import objgraph

# https://mg.pov.lt/objgraph/

from package.module_a import A1

a1 = A1()
objgraph.show_backrefs([a1], filename='sample-backref-graph.png')

# print()
dict_all_link = A1.dict_ref
# obj = A1.dict_ref["package.module_c.C"][0]()
# gc.get_referrers(obj) # кто ссылается на obj
# print(sys.getrefcount(obj))
# print(gc.get_referents(obj)) # на что ссылается obj

for ind, ins_c_i in enumerate(A1.dict_ref["package.module_c.C"]):
    print("#" * 10)
    for ref_i in gc.get_referrers(ins_c_i()):
        print(ref_i)
        print(gc.get_referents(ref_i))
        objgraph.show_backrefs([ref_i], filename=f'{ind}.png')

# for i in gc.get_referrers(A1.dict_ref["package.module_c.C"][0]()):  # obj
#     print(i)

print()
