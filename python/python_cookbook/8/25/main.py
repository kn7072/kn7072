import logging

# Поддержка кеширования
import weakref
_spam_cache = weakref.WeakValueDictionary()

a = logging.getLogger('foo')
b = logging.getLogger('bar')
c = logging.getLogger('foo')

print(a is b)
print(a is c)
list(_spam_cache)
del a
del c
list(_spam_cache)
del c
list(_spam_cache)


# Опрашиваемый класс
class Spam:
    def __init__(self, name):
        self.name = name


def get_spam(name):
    if name not in _spam_cache:
        s = Spam(name)
        _spam_cache[name] = s
    else:
        s = _spam_cache[name]
    return s


a = get_spam('foo')
b = get_spam('bar')
c = get_spam('foo')
print(a is b)
print(a is c)
