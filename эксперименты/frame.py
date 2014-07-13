import traceback
def f():
  for i in range(10):
        yield i
def k():
    q = traceback.extract_stack()
    print (7)
def d():
    #for i in range(10):
    #traceback.print_stack()
    k()
    print (3)
i = f()
j = d()
print ()
######################
def a(x=5):
    print (x)

a()
a(4)
a()
######################
class r:
    def e(self, w):
        print (w)
w = r()
w.e(3)
setattr(w, 'c' , 5)
print (w.c)
w.__class__.e.__get__(w)(8)