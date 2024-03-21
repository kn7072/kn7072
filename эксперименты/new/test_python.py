# -*- coding:utf-8 -*-
def fun(arg1, agr2):
    print(arg1)

def fun2(arg1):
    print(arg1)

c = [2, 4]
b = [1,2,3,4,5,6,7,8,9,10]
x = [b.__iter__()]

fun(*c)
fun2(*[b.__iter__()])
d = list(zip(b.__iter__(), b.__iter__()))
iter_t = b.__iter__()
t = list(zip(iter_t, iter_t))
print(t)
