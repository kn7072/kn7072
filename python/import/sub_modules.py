# -*- coding: utf-8 -*-

# https://digitology.tech/docs/python_3/reference/import.html#id14

"""

5.4.2. Подмодули¶

Когда подмодуль загружается с использованием любого механизма (например, API importlib, операторов import или 
import-from или встроенного __import__()), привязка помещается в пространство имён родительского модуля к объекту подмодуля. 
Например, если в пакете spam есть подмодуль foo, после импорта spam.foo у spam будет атрибут foo, связанный с подмодулем. 
Допустим, у вас есть следующая структура каталогов:

spam/
    __init__.py
    foo.py
    bar.py

а в spam/__init__.py есть следующие строки:

from .foo import Foo
from .bar import Bar

затем выполнение следующего, помещает привязку имени к foo и bar в модуле spam:

>>> import spam
>>> spam.foo
<module 'spam.foo' from '/tmp/imports/spam/foo.py'>
>>> spam.bar
<module 'spam.bar' from '/tmp/imports/spam/bar.py'>

Учитывая знакомые правила связывания имён Python — это может показаться удивительным, 
но на самом деле это фундаментальная особенность системы импорта. 
Инвариантное удержание состоит в том, что если у вас есть sys.modules['spam'] и 
sys.modules['spam.foo'] (как после вышеупомянутого импорта), последний должен отображаться как атрибут foo первого.

"""
import sys
import spam

print(spam.foo)
print(spam.bar)

print(sys.modules.get("spam"))
print(sys.modules.get("spam.foo"))

print(spam.__spec__)
print(getattr(spam, "__path__"))  # пакет
print(getattr(spam.foo, "__path__", "False")) # модуль