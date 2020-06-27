from module_1 import fun, w
x = 17
w = 7
class A():
    x = 3
    def a(self):
        print(x, w)
        print(self.x)

def f(j):
    print(j)
z = A()
fun(z.a)
fun(f)
print()