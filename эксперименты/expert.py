# class Base(object):
#   def __init__(self):
#     print("Base created")
# class Child(Base):
#   def __init__(self):
#     Child.__bases__[0].__init__(self)
#     print("Child created")
# b = Base()
# c = Child()

# class Base(object):
#   def __init__(self):
#    print("Base created")
# class Child(Base):
#   def __init__(self):
#     super(Child, self).__init__()
#     print("Child created")
# b = Base()
# c = Child()
# print()
class Base(object):
  def __init__(self):
    print("Base created")
class Child(Base):
  def __init__(self):
    super(Child).__init__()
    print("Child created")
b = Base()
c = Child()
print()
# class Base(object):
#   def __init__(self):
#     print("Base created")
# class Child(Base):
#   def __init__(self):
#     super().__init__()
#     print("Child created")
# b = Base()
# c = Child()
#
# class Base(object):
#   def __init__(self):
#     print("Base created")
# class Child(Base):
#   def __init__(self):
#     Base.__init__(self)
#     print("Child created")
b = Base()
c = Child()
print()
x = 7
y = -17
str = 'This is a very long test'
out = str[:x]+' not'+str[y:]
print(out)
#######################################
def foo(n):
    if (n < 3):
        yield 1
    else:
        return
    yield 2

n = 2
f = foo(n)
for i in range(n): print(f.__next__())

# n = 5
# f = foo(n)
# for i in range(n): print(f.__next__())
############################################
class MyError(Exception): pass

class MySubError(MyError): pass

try:
    raise MySubError()
except MyError: print("MyError")
except MySubError:
    print("MySubError")
except Exception: print("Exception")

##############################################
def gener(b):
        b += 1
        yield b

a = 0
g = gener(a)
print(g.__next__())

############################################
def recurse(i, n=0):
        if (n <= 50):
                print(n)
                recurse(n+n, i*i)
        else:
                print(n)

recurse(1)
##########################################
dict1 = {'Julie' : 8570, 'Kim' : 7540, 'Tiffany' : 7030, 'Gretchen' : 9080, 'Pam' : 9090}
dict2 = {'Julie' : 85, 'Kim' : 100, 'Tiffany' : 70, 'Gretchen' : 70, 'Pam' : 95}

first = 'Pam'
second = 'Julie'
third = 'Jaime'

if (dict1.keys() == dict2.keys()):
        print("dict1 and dict2 have the same keys")

if (third in dict2.keys()):
        print("third is in dict2")

print(sorted(dict2))

if (first not in dict2.keys()):
        print("first is not in dict2")
###############################################
dict1 = {'key1' : 'val1', 'key2' : 'val2', 'key3' : 'val3'}
dict2 = {'key1' : 'val1', 'key3' : 'val3', 'key5' : 'val5'}

dict3 = dict1.update(dict2)

print(dict1)
print(dict2)
print(dict3)
################################################
try:
    try: 1/0
    finally: print('Inner Block')
except ArithmeticError: print('Arithmetic Error')
except ZeroDivisionError: print('Zero Division Error')
except: print('Other Error')
print('###################################################')
class A: pass
class B(A): pass
class C(object): pass
class D(C): pass
class K:pass
a = A()
b = B()
c = C()
d = D()

print(isinstance(a, type(b)))
print(issubclass(C, C))
print(isinstance(d, D))
print(issubclass(C, (K, D, A, B, C)))
print('###################################################')
var1 = 0
var2 = 0
var3 = 0
with open('tmp', 'w') as file:
        file.write("line 1\n")
        var1 = file.tell()
        file.close()
with open('tmp', 'a') as file:
        file.write("line 2\n")
        var2 = file.tell()
        file.close()
with open('tmp', 'a') as file:  # r+
        file.seek(var1)
        var5 = file.tell()
        file.write("line 3\n")
        file.close()
with open('tmp', 'a') as file:  # r+
        file.seek(var2, var3)
        var6 = file.tell()
        file.write("line 4\n")
        file.close()
print('###################################################')
lst = [1,2]
dct = {4:5,6:7}

d = {
         #lst:(3,4),            # line 1
         (5,6):[7,8],          # line 2
         None:23,              # line 3
         23:None,              # line 4
         0:0,                  # line 5
         "this":{1:2,3:4},     # line 6
         #dct:"that"            # line 7
}
print('###################################################')
def g(y, t):
  g.s = "some string"
  return y % t
# try:
#   print('#1:', g.s)
# except Exception as e:
#   print(str(e))
# try:
#   print('#2:', g.__dict__)
# except Exception as e:
#   print(str(e))
# g(5, 3)
# try:
#   print('#3:', g.s)
# except Exception as e:
#   print(str(e))
# try:
#   print('#4:', g.__dict__)
# except Exception as e:
#   print(str(e))
print('###################################################')
class A:
 def __init__(self, a='A', b='B'):
   self.a = a
   self.b = b
class C(object):
 pass
a = A(a=1, b=2)
c = C()
print('#1:',list(zip([1, 2, 3], ['a', 'b', 'c'], ['A', 'B', 'C'])))
print('#2:',vars(a))
print('#3:',vars(c))
print('#4:',type(a))
print('#5:',type(A))
print('#6:',type(c))
print('#7:', sum(range(1,10)))
print('###################################################')
baselist = ['apple', 'orange', 'banana', 'kiwi', 'strawberry']
class SimpleSequence:
  def __init__(self,data):self.data = data
  def __getitem__(self,i):return self.data[i]
  def __setitem__(self,i, val):self.data[i] = val
  def __delitem__(self,i):del self.data[i]
  def __len__(self):return len(self.data)
simpleseq = SimpleSequence(baselist)
simpleseq[0] == 'apple'           # Line 1
simpleseq[1] != 'banana'          # Line 2
simpleseq[2:-1] == baselist[2:-1] # Line 3
len(simpleseq) == len(baselist)   # Line 4
print('###################################################')
def SomeFunction(y):
 x = 0
 try:
   x = y/0
 except (ArithmeticError, ZeroDivisionError):
   print('Divide by Zero')
 return x

try:
 SomeFunction(1)
finally:
 pass
 #CleanupFunction() ERROR

dict1 = {'Julie' : 8570, 'Kim' : 7540, 'Tiffany' : 7030, 'Gretchen' : 9080, 'Pam' : 9090}
dict2 = {'Julie' : 85, 'Kim' : 100, 'Tiffany' : 70, 'Gretchen' : 70, 'Pam' : 95}

first = 'Pam'
second = 'Julie'
third = 'Jaime'

if (dict1.keys() == dict2.keys()):
        print("dict1 and dict2 have the same keys")

if (third in dict2.keys()):
        print("third is in dict2")

print(sorted(dict2))

if (first not in dict2.keys()):
        print("first is not in dict2")

print(sorted(list(dict1)))
print('###################################################')
def f(a, lst=[]):
    lst.append(a)
    return lst
print(f(1))
print(f(2))
print(f(3))
print('###################################################')
class ValueHolder(object):
    __slots__ = ['value']
    def __init__(self, val):
        self.value = val

class A(ValueHolder):
    @classmethod
    def clsmeth(obj1, obj2):
        obj1.value = obj2
    @staticmethod
    def sttcmeth(obj1, obj2):
        obj1.value = obj2

class B(A): pass

va = ValueHolder(67)
vb = ValueHolder(83)
a = A(67)
b = B(83)
# a.clsmeth(va, 98)   # Line 1
# b.clsmeth(vb, 98)   # Line 2

a.sttcmeth(va, 13)  # Line 3
b.sttcmeth(vb, 13)  # Line 4

a.clsmeth(21)   # Line 5
b.clsmeth(21)   # Line 6

# a.sttcmeth(101)     # Line 7
# b.sttcmeth(101)     # Line 8
print('###################################################')
def foo():               # Line 1
   print('sss')
   for i in range(5):    # Line 2
       yield 3*i         # Line 3

for x in foo():
    print(x)
a = foo()                # Line 4
print(a.__next__())      # Line 5
print(a.__next__())      # Line 6

print(a)                 # Line 7
a.__next__()             # Line 8
print('###################################################')
def gen():
        a, b = 0, 1
        print("start generator loop")
        for i in range(10):
                yield b
                a, b = b, a+b
        print("end generator loop")
        return 999

G = gen()
for i in G:
    print(i)
print(G.__next__())