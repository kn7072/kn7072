from module_1 import fun, function

from module_1 import x, fun_2
x=5
fun_2()
print(x)
class A():
    x = 3
    def a(self):
        print(self.x)
    def b():
        print(x)
def simple_fun():
        print(x)
def f(j):
    print(j)
z = A()
A.b()
function(z.a)
function(A.b)
function(simple_fun)
fun(z.a)
fun(f)
print()