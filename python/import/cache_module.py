# -*- coding: utf-8 -*-

"""
https://digitology.tech/docs/python_3/reference/import.html
"""



import sys

"""
Во время импорта имя модуля ищется в sys.modules, и, если оно присутствует, связанным значением является модуль, 
удовлетворяющий импорту и процесс завершается. Однако, если значение равно None, то вызывается ModuleNotFoundError. 
Если имя модуля отсутствует, Python продолжит поиск модуля.

sys.modules доступен для записи. 
Удаление ключа может не уничтожить связанный модуль (поскольку другие модули могут содержать ссылки на него), 
но сделает недействительной запись в кеше для названного модуля, заставляя Python заново искать указанный модуль 
при его следующем импорте. Ключ также может быть назначен None, в результате чего следующий импорт модуля приведет к ModuleNotFoundError.

Однако будьте осторожны: если вы сохраните ссылку на объект модуля, сделаете недействительной его запись в кэше в sys.modules, 
а затем повторно импортируете нужный модуль, два объекта модуля не будут одинаковыми. 
Напротив, importlib.reload() будет повторно использовать объект того же модуля и просто повторно инициализировать содержимое модуля, 
повторно запустив код модуля.
"""
print(f"{sys.modules.get('gc')}")

import gc
print(f"{sys.modules.get('gc')}")
# del sys.modules["gc"]

