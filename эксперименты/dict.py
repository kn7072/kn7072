class S:
    def __init__(self):
        print("S")

class D:
    def __init__(self):
        print("D")

class X(S, D):
    pass

y = X




def x(y):
    while True:
        y -= 1
        print(y)
        if y < 0:
            break
    return y

x(10)

a = 10
def dec(s):
    w = dict(s.__dict__)
    w['comand_args'] = 100
    x = type('s', (s,), w)
    return x
def s(fun):
    fun()
@dec
class StuffHolder:
    stuff = "class stuff"

a = StuffHolder()
b = StuffHolder()
a.stuff     # "class stuff"
b.stuff     # "class stuff"

b.b_stuff = "b stuff"
b.b_stuff   # "b stuff"

StuffHolder
print('d')