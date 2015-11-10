# -*- coding:utf-8 -*-
arr = [1, 2, 3, 4, 5, 6, 7, 7, 7]
arr_2 = [1,2]
arr_3 = [1, 3, 5]
x = (i for i in arr)
y = [i for i in arr]
z = {i for i in arr}

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
def counter(n):
    while True:
        yield n
        n += 1
#squares = [i*i for i in counter(1)][0:10]

# class A(object):
#   def __init__(self):
#       super(self.__class__, self).__init__()

def fibo(i):
    last_0 = 0
    fibo_1 = 1
    #print(fibo_)
    for j in range(i):
        fibo_ = last_0 + fibo_1
        last_0 = fibo_1
        fibo_1 = fibo_
        print(fibo_)

def fibo_2(i):
    a,b = 0, 1
    for i in range(i):
        yield b
        a, b = b, a+b


fibo(10)
# print(list(fibo_2(5)))
# Есть три отрезка. Надо написать Unit-test, который проверяет могут ли они составлять треугольник.
#old_3 = arr[::3]
x = [i for i in range(99)]

def man(ls, index):
    if len(ls) == 1:
        return ls
    else:
        ss = len(ls) % 2
        ls = ls[index::2]

        if ss == 0:
            res = man(ls, 0)
        else:
            res = man(ls, 1)
        return res

uu = list(range(1,7))
e = man(uu, 0)
print(e)
print()