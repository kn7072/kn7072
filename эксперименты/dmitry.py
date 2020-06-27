# -*- coding: utf-8 -*-
class A:
    def __init__(self, data):
        super().__init__()
        self.__b = data
        self.c = data

    def __getitem__(self, key):
        return self.c[key]

dict_ = {'x': 4}
a = A(dict_)
t = a['x']

xx = ['z', 'b']
yy = [1, 3]
tt = dict(zip(xx, yy))
print(tt)
# "l:\Development\Литература по тестированию\Security\Grossman.XSS Atacks. Exploits and Defence.pdf"
# https://www.owasp.org/index.php/Testing_for_Input_Validation
