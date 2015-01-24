def make_action():
    acts = []
    for i in range(5):
        acts.append(lambda x: i**x)
    return acts
acts = make_action()
print(acts[0](2), acts[2](2), acts[4](2))
print()

class Super:
    def method(self):
        print('in Super.method')
    def delegate(self):
        self.action()
    def __getattr__(self, item):
        print('game over :)')
class Provider(Super):
    def action(self):
        print('in Provider.action')
x = Provider()
x.delegate()

def lister(lst=[]):
    lst.append([1,2,3])
    print(lst)
lister(), lister()


############################################
class A:
    def fun(self):
        print('fun_A')
class X(A):
    pass
class B(A):
    def fun_(self):
        print('fun_B')
class C:
    def fun(self):
        print('fun_C')

class E(B,C):
    pass
e = E()
e.fun()
class A:
    def fun(self):
        print('fun_A')
class X(A):
    pass
class B(X):
    def fun_(self):
        print('fun_B')
class C(X):
    def fun(self):
        print('fun_C')

class E(B,C):
    pass
e = E()
e.fun()
#############################################
var = 10

def fun_1():
    var = 7
    print(var)

def fun_2():
    var = 5
    global var
    print(var)

def fun_3():
    print(var)
fun_1(), fun_2(), fun_3()
###################################
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
#################################
def d1(f):return lambda : 'x'+f()
def d2(f):return lambda : 'y'+f()
def d3(f):return lambda : 'z'+f()
@d1
@d2
@d3
def fun():
    return 'hallo world'
print(fun())

################################
class A:
    @staticmethod
    def fun(x):
        print(x)

a = A().fun(5)
A.fun(3)
################################
class A:
    var = 1
    def __init__(self):
        self.var = 10
    @classmethod
    def fun(self, x):
        print(self.var)

a = A().fun(5)
A.fun(3)