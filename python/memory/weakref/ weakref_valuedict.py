import gc
from pprint import pprint
import weakref

# Листинг 2.71. weakref__valuedict.py - Хелман - Стандартная библиотека Pytho 3


gc.set_debug(gc.DEBUG_UNCOLLECTABLE)


class ExpensiveObject:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'ExpensiveObject({})'.format(self.name)
    
    def __del__(self):
        print('(Deleting {})'.format(self))


def demo(cache_factory):
    # Удержать объекты для того, чтобы предотвратить
    # немедленное удаление слабых ссылок

    all_refs = {}
    #  Создать кеш, используя функцию-фабрику
    print('CACHE TYPE:', cache_factory)
    cache = cache_factory()
    for name in ['one', 'two', 'three']:
        obj = ExpensiveObject(name)
        cache[name] = obj
        all_refs[name] = obj
        del obj  # уменьшить счетчик ссылок

    print(' all_refs =', end=' ')
    pprint(all_refs)
    print('\n Before, cache contains:', list(cache.keys()))
    for name, value in cache.items():
        print(' {} = {}'.format(name, value))
        del value  # уменьшить счетчик ссылок

    # Удалить все ссылки на объекты, за исключением тех,
    # которые находятся в кеше
    print('\n Cleanup:')
    del all_refs
    gc.collect()

    print('\n After, cache contains:', list(cache.keys()))
    for name, value in cache.items():
        print(' {} - {}'.format(name, value))
        print(' demo returning')
    return


demo(dict)
print()
demo(weakref.WeakValueDictionary)
