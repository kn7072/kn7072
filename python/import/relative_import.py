# -*- coding: utf-8 -*-

# https://digitology.tech/docs/python_3/reference/import.html#relativeimports

"""
5.7. Относительный импорт пакетов
Относительный импорт использует начальные точки. Одиночная точка в начале указывает на относительный импорт, 
начиная с текущего пакета. Две или более точки в начале указывают на относительный импорт в родительский(-ые) пакет(-ы) 
текущего пакета, по одному уровню на точку после первого. Например, учитывая следующий макет пакета:

package/
    __init__.py
    subpackage1/
        __init__.py
        moduleX.py
        moduleY.py
    subpackage2/
        __init__.py
        moduleZ.py
    moduleA.py

В subpackage1/moduleX.py или subpackage1/__init__.py следующие допустимые значения относительного импорта:

from .moduleY import spam
from .moduleY import spam as ham
from . import moduleY
from ..subpackage1 import moduleY
from ..subpackage2.moduleZ import eggs
from ..moduleA import foo

Абсолютный импорт может использовать синтаксис import <> или from <> import <>, 
но относительный импорт может использовать только вторую форму; причина в том, что:

import XXX.YYY.ZZZ

должен предоставлять XXX.YYY.ZZZ как используемое выражение, но .moduleY не является допустимым выражением.

"""