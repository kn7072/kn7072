# -*- encode: utf-8 -*-
i = 1
j = 1
class P1():
    def __init__(self):
        global i
        print(str(i)+" i")
        i+=1
class P2():
    def __init__(self):
        global j
        print(str(j)+" j")
        j+=1
class A(P1, P2):
    def __init__(self):
        # something
        P1.__init__(self)
        P2.__init__(self)
class B(P1, P2):
    def __init__(self):
        # something
        P1.__init__(self)
        P2.__init__(self)
class C(B, A):
    def __init__(self):
        # something
        print(type(self).mro())
        super().__init__()  # заходим только в B
        # B.__init__(self)
        # A.__init__(self)

c = C()