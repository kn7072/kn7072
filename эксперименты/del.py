import sys
# del x и x.__del__()
# del x не является прямым вызовом x.__del__() - первая форма сокращает количество ссылок на объект x на одну,
# тогда как последний метод вызывается только когда количество ссылок достигает нуля..


class A:

    def __init__(self, name):
        self.name = name
        print('create '+str(sys.getrefcount(self))+' copies')
    def __del__(self):
        print(self.name)

aa = [A(str(i)) for i in range(3)]
aa = [A(str(i)) for i in ('asdfasdfasdf', 'qwerqwerqwer', 'zxcvzxcvzcxv')]
del aa
aa = [A(str(i)) for i in range(3)]
del aa[0]
del aa[0]
del aa[0]
aa = [A(str(i)) for i in range(3)]
sys.getrefcount(aa[0])
for a in aa:
	print('now we have '+str(sys.getrefcount(a))+' copies')
	del a
aa
######################################################################
dict_revers = {}
dict_revers2 = {}
dict_ = {"a": 1, "b": 2, "c": 3}
for key, value in dict_.items():
    dict_revers[value] = key
dict_revers2 = dict((value, key) for key, value in dict_.items())
######################################################################

def addition_range(i, k):
    temp_func = []
    for j in range(i, k):
        temp_func.append(lambda y, x=j: (x+y))
    return temp_func

list_func = addition_range(0, 5)
######################################################################
import itertools
i1 = iter([1, 2, 3])
i2 = iter([4, 5])
i3 = iter((6, 7, 8))
def chain(*args):
    for x in itertools.chain(*args):
        yield x


c = chain(i1, i2, i3, iter('iter'))
#c.__next__()
for i in c:
    print(i)
c.next()
print()