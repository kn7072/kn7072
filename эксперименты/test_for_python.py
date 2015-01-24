# -*- coding:utf-8 -*-

class X:
    def __init__(self, temp_dict):
        self.temp_dict = temp_dict
    # def __call__(self, *args, **kwargs):
    #     return self.temp_dict
    def __getattr__(self, item):
        return getattr(self.temp_dict, item)
    def __getitem__(self, key):
        return self.temp_dict[key]
    def __str__(self):
        return self.temp_dict
x = X({'one': 1, 'two': 2, 'three': 3})
x['one']

print()
#####################################################
class Meta_iter(type):
    def __iter__(cls):
        print('cls {0}'.format('dddddd'))
        return iter(cls.list_instance)

class Reg(metaclass=Meta_iter):

    instance = None
    list_instance = []
    def __init__(self):
        type(self).list_instance.append(self)

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance

    # def __next__(self):
    #     return type(self).list_instance.next()
    def __iter__(self):
        # for i in type(self).list_instance:
        #     yield i
        print('dddddd')
        return iter(type(self).list_instance)

r1 = Reg()
r2 = Reg()
r3 = Reg()
for i in Reg:
    print(i)