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