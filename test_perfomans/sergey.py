class B():
    c = 1

class A():
    b = B()
    def __init__(self):
        self.b.c = 2
a = A()
print(a.b.c)
t = A()
print(A.b.c)
print()