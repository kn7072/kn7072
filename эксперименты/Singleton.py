class D():
    q = 3
    def __init__(self):
        self.w = 15
    def __call__(self, *args, **kwargs):
        print ("hallo")

class Singleton(D):
        obj = None
        def __new__(cls,*dt,**mp):
           if cls.obj is None:
              cls.obj = D.__new__(cls,*dt,**mp)
           return cls.obj

        def __init__(self):
            D.__init__(self)
            self.x = 5

class A(object):
    _dict = dict()

    def __new__(cls):
        if 'key' in A._dict:
                print ("EXISTS")
                return A._dict['key']
        else:
                print ("NEW")
                return super(A, cls).__new__(cls)

    def __init__(self):
        print ("INIT")
        if bool(A._dict):  # запрет на переинициализацию
            return None
        A._dict['key'] = self
        self.r = 5
        print ("")

class B():
    s = A().__dict__
    x = type('D',(D,), s) #{}

if __name__ =="__main__":
    d = D()
    b = B()
    a1 = A()
    a1.r = 10
    a2 = A()
    a2.t = 9
    a3 = A()

    obj = Singleton()
    obj.attr = 12
    new_obj = Singleton()
    new_obj.attr
    new_obj.attr = 10
    new_obj.wwww = "fffffffff"
    pass