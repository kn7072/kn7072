# -*- codind:utf-8 -*-

class GetAttr:
    def __init__(self, obj):
        self.obj = obj
        print(id(obj))

    def __getattr__(self, item):
        return getattr(self.obj, item)


array = []
print(id(array))
get = GetAttr(array)
append = get.append
append(5)
print(array)