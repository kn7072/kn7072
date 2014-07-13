# -*- coding: utf-8 -*-
class C1:
    def meth1(self):
        self.__X = 88     # Теперь X - мой атрибут
    def meth2(self):
        print(self.__X)   # Превратится в _C1__X

class C2:
    def metha(self):
        self.__X = 99     # И мой тоже
    def methb(self):
        print(self.__X)   # Превратится в _C2__X

class C3(C1, C2): pass
                              # В I два имени X
if __name__=="__main__":
    I = C3()
    I.meth1()
    I.metha()
    print(I.__dict__)
    I.meth2()
    I.methb()
