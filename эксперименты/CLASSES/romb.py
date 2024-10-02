# coding: utf-8

"""Тестируем ромбическое наследование"""


class X:
    pass

class G(X):

    def a(self) -> None:
        """"""
        print("G")


class A(G):
    """"""
    pass


class B(X):

    def a(self) -> None:
        """"""
        print("B")


class C(A, B):
    pass


c = C()
c.a()