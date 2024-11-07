# -*- coding:utf-8 -*-
class A:
    def x(self):
        print("s")


setattr(A, "w", 7)
A.__dict__["e"] = 5
print()
