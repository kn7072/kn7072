# -*- coding: utf-8 -*-


def method(a):
    print(a)


class B():
    var = 10

    def method_b(self):
        print(self.var)

CLASS = type('A', (B,), {'method_a': method})
a = type(B).__call__(B)  # a instance class B
# ERROR c = type(B).__call__()
print()



