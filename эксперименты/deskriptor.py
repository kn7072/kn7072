# -*- coding: utf-8 -*-
class RevealAccess(object):
    """
        Пример data дескриптора, который присваивает
        и возвращает значение переменной, а также печатает
        историю доступа к переменной.
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print ('Получаю значение', self.name)
        return self.val

    def __set__(self, obj, val):
        print ('Присваиваю значение' , self.name)
        self.val = val

class MyClass(object):
    x = RevealAccess(10, 'var "x"')
    def met(self):
        pass
    y = 5

m = MyClass()
e = m.x
t = m.met
descr = RevealAccess(10, 'var "x"')
descr.__get__(m)
print()