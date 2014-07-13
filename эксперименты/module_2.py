from module_1 import fun

class A():
    x = 3
    def a(self):
        print(self.x)

def f(j):
    print(j)
z = A()
fun(z.a)
fun(f)
print()