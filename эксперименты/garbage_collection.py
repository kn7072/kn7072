# -*- coding:utf-8 -*-
import gc
# http://asvetlov.blogspot.ru/2013/05/gc.html
import weakref  # для создания слабых ссылок
import sys


class A:
    pass


frame = sys._getframe()  # [номер кадра стека]
a = A()
count_ref = sys.getrefcount(a)  # 2


def del_obj():
    print("объект удален")
ar = weakref.ref(a, del_obj)
new_count_ref = sys.getrefcount(a)  # 2
ar()  # возвращает объект a
print()


class Node(object):
    parent = None

    def __init__(self, *children):
        self.children = list(children)
        for node in self.children:
            node.parent = self

    @classmethod
    def tree(cls, depth=1, numchildren=1):
        if depth == 0:
            return []
        return [cls(*cls.tree(depth-1, numchildren)) for _ in range(numchildren)]


def gc_cb(phase, info):
    """Добавляем garbage collection hook для того чтобы увидеть когда срабатывает сборщик мусора и сколько
    объектов он уничтожает:"""
    if not info['collected'] and not info['uncollectable']:
        return
    print("{0}:\t{1[generation]}\t{1[collected]}\t{1[uncollectable]}".format(phase, info))

gc.callbacks.append(gc_cb)

# Наконец, делаем много-много наших деревьев и смотрим как они разрушаются:
# Пороги стоят стандартные:
gc.get_threshold()  # (700, 10, 10) 700 объектов в нулевом поколении и по 10 в первом и во втором.
for n in range(20):
    for _ in range(n):
        Node.tree(depth=5, numchildren=6)