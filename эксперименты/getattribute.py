import unittest
class Getattribute():
   def __init__(self,func):
       self.func = func
   def __call__(self, *args, **kwargs):
       self.func(*args, **kwargs)

class x(unittest.TestCase):
    def t(self, e):
        print (e)

    def __getattribute__(self,name):
        if not name.startswith("assert_that") and name.startswith("assert"):
            return Getattribute(object.__getattribute__(self, name))
        else:
            if name== 't':
                return object.__getattribute__(self,name)
            return object.__getattribute__(self,name)
if __name__=="__main__":
    r = x()
    r.t
    r.assertEquals(3,3,"значения не совпадают")
    r.t('vvv')
