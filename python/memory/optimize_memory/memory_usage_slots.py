# -*- coding: utf-8 -*-

# https://gist.github.com/MartinHeinz/7d539e53f67273a2670b43451052eaea#file-memory_usage_slots-py


from pympler import asizeof

# Your Python Objects Use
# https://code.tutsplus.com/tutorials/understand-how-much-memory-your-python-objects-use--cms-25609
"""
Small Objects

CPython manages small objects (less than 256 bytes) in special pools on 8-byte boundaries. 
There are pools for 1-8 bytes, 9-16 bytes, and all the way to 249-256 bytes. 
When an object of size 10 is allocated, it is allocated from the 16-byte pool for objects 9-16 bytes in size. 
So, even though it contains only 10 bytes of data, it will cost 16 bytes of memory. 
If you allocate 1,000,000 objects of size 10, you actually use 16,000,000 bytes 
and not 10,000,000 bytes as you may assume. This 60% extra overhead is obviously not trivial.
"""

class Normal:
    a = 10


class Smaller:
    __slots__ = ('foo',)
    # foo = 10


# О слотах https://habr.com/ru/post/686220/
"""
Поскольку каждый объект в Python содержит динамический словарь, который позволяет добавлять атрибуты. 
Для каждого объекта экземпляра у нас будет экземпляр словаря, который потребляет больше места и тратит много оперативной памяти. 
В Python нет функции по умолчанию для выделения статического объема памяти при создании объекта для хранения всех его атрибутов.

Использование slots уменьшает потери пространства и ускоряет работу программы, выделяя пространство для фиксированного количества атрибутов.


Ну и под конец важные выводы:

    Без переменной словаря dict, экземплярам нельзя назначить атрибуты, не указанные в определении slots. При попытке присвоения имени переменной, не указанной в списке, вы получите ошибку AttributeError. Если требуется динамическое присвоение новых переменных, добавьте значение 'dict' в объявлении атрибута slots.

    Атрибуты slots, объявленные в родительских классах, доступны в дочерних классах. Однако дочерние подклассы получат dict, если они не переопределяют slots.

    Если класс определяет слот, также определенный в базовом классе, переменная экземпляра, определенная слотом базового класса, недоступна. Это приводит к неоднозначному поведению программы.

    Атрибут slots не работает для классов, наследованных, от встроенных типов переменной длины, таких как int, bytes и tuple.

    Атрибуту slots может быть назначен любой нестроковый итерируемый объект. Могут использоваться словари, значениям, соответствующим каждому ключу, может быть присвоено особое значение.

    Назначение class работает, если оба класса имеют одинаковые slots.

    Может использоваться множественное наследование с несколькими родительскими классами с разделением на слоты, но только одному родительскому элементу разрешено иметь атрибуты, созданные с помощью слотов (другие классы должны иметь макеты пустых слотов), нарушение вызовет исключение TypeError.
"""


class SmallerChild(Smaller):
    __slots__ = ('__dict__',)
    pass


print(asizeof.asized(Normal(), detail=1).format())
# <__main__.Normal object at 0x7f3c46c9ce50> size=152 flat=48
#     __dict__ size=104 flat=104
#     __class__ size=0 flat=0

print(asizeof.asized(Smaller(), detail=1).format())
# <__main__.Smaller object at 0x7f3c4266f780> size=32 flat=32
#     __class__ size=0 flat=0

print(asizeof.asized(SmallerChild(), detail=1).format())
# <__main__.SmallerChild object at 0x7fd279ea5fc0> size=160 flat=56
#     __dict__ size=104 flat=104
#     __class__ size=0 flat=0


small_child = SmallerChild()
small_child.x = 10
print(asizeof.asized(small_child, detail=1).format())
small_child.y = 10
print(asizeof.asized(small_child, detail=1).format())
small_child.z = 10
print(asizeof.asized(small_child, detail=1).format())