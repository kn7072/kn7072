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
aa = [A(str(i)) for i in ('asdfasdfasdf','qwerqwerqwer','zxcvzxcvzcxv')]
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
