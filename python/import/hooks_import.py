# -*- coding: utf-8 -*-

# https://digitology.tech/docs/python_3/reference/import.html#id9


"""

5.3.3. Хуки импорта

Машинерия импорта разработана с возможностью расширения; основным механизмом для этого является хуки импорта. 
Есть два типа хуков импорта: мета хуки и хуки путей импорта.

Мета-хуки вызываются в начале обработки импорта, до того, как произойдет какая-либо другая обработка импорта, 
кроме поиска в кэше sys.modules. Это позволяет мета-хукам отменять обработку sys.path, замороженные модули или даже встроенные модули. 
Мета-хуки регистрируются путём добавления новых объектов поиска в sys.meta_path, как описано ниже.

Хуки пути импорта вызываются как часть обработки sys.path (или package.__path__) в точке, где встречается связанный с ними элемент пути. 
Хуки пути импорта регистрируются путём добавления новых вызываемых объектов в sys.path_hooks, как описано ниже.

5.3.4. Мета путь
Если требуемый модуль не найден в sys.modules, Python выполняет поиск в sys.meta_path, который содержит список объектов поиска мета-пути. 
Эти средства поиска опрашиваются, чтобы узнать, знают ли они, как обращаться с указанным модулем. Поисковики мета-пути должны реализовать метод 
под названием find_spec(), который принимает три аргумента: имя, путь импорта и (необязательно) целевой модуль. Поисковик мета-пути может 
использовать любую стратегию, чтобы определить, может ли он обрабатывать требуемый модуль или нет.

Если средство поиска мета-пути знает, как обрабатывать требуемый модуль, он возвращает объект спецификации. Если он не может обработать указанный модуль, 
он возвращает None. Если обработка sys.meta_path достигает конца своего списка без возврата спецификации, то вызывается ModuleNotFoundError. 
Любые другие возникшие исключения просто распространяются, прерывая процесс импорта.

Метод поиска мета-пути find_spec() вызывается с двумя или тремя аргументами. 
Первое — это полное имя импортируемого модуля, например foo.bar.baz. 
Второй аргумент — это записи пути, используемые для поиска модуля. Для модулей верхнего уровня второй аргумент - None, 
    но для подмодулей или подпакетов второй аргумент — это значение атрибута __path__ родительского пакета. 
    Если соответствующий атрибут __path__ недоступен, создается ModuleNotFoundError. 
Третий аргумент — это существующий объект модуля, который будет загружен позже. Система импорта передает целевой модуль только во время перезагрузки.

Мета-путь может быть пройден несколько раз для одного запроса на импорт. Например, предполагая, что ни один из задействованных модулей ещё не был кэширован, 
при импорте foo.bar.baz сначала выполняется импорт верхнего уровня, вызывая mpf.find_spec("foo", None, None) для каждого средства поиска мета-пути (mpf). 
После импорта foo будет импортирован foo.bar путём повторного прохождения мета-пути с вызовом mpf.find_spec("foo.bar", foo.__path__, None). 
После импорта foo.bar окончательный обход вызовет mpf.find_spec("foo.bar.baz", foo.bar.__path__, None).

Некоторые средства поиска мета-пути поддерживают только импорт верхнего уровня. Эти импортеры всегда будут возвращать None, 
если в качестве второго аргумента передается что-либо, кроме None.

По умолчанию в Python sys.meta_path есть три средства поиска мета-пути: 
    один знает, как импортировать встроенные модули, 
    второй знает, как импортировать замороженные модули, 
    а другой знает, как импортировать модули из путей импорта (то есть поисковик на основе пути).

Изменено в версии 3.4: Метод поиска мета-пути find_spec() заменил устаревший find_module(). 
Хотя он будет продолжать работать без изменений, механизм импорта попробует его, только если поисковик не реализует find_spec().

"""

# https://www.sobyte.net/post/2021-10/python-import/

import sys
from pprint import pprint
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec


pprint(sys.meta_path)


class NoSuchModuleFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        return ModuleSpec('nosuchmodule', None)


sys.meta_path = [NoSuchModuleFinder()]

"""
As you can see, the ModuleNotFound exception is not thrown when we tell the system how to find_spec. 
But to successfully load a module, a loader loader is also needed.
"""
# import nosuchmodule