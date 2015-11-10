class B():
    c = 1
class A():
    b = B()
    e = 100
    def __init__(self):
        self.b.c = 2
    def x(self):
        self.b = 10
        setattr(self.__class__,'e', 5)
a = A()
print(a.b.c)
t = A()
print(A.b.c)
print()

z = A()
z.x()
z.b