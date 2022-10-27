# coding: utf-8

# 9.5. Определение декоратора с настраиваемыми пользователем атрибутами

import logging
from functools import partial, wraps


# Вспомогательный декоратор для прикрепления
# к функции в качестве атрибута obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func


def logged(level, name=None, message=None):
    '''
    Добавляет логирование в функцию. level – это уровень логирования,
    name – это название логгера, message – это сообщение в лог. Если
    name и message не определены, они будут дефолтными от имени функции
    и ее модуля.
    '''

    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)

        # Прикрепляем функции-сеттеры
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel

        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg

        return wrapper

    return decorate


# Пример использования
@logged(logging.DEBUG)
def add(x, y):
    return x + y


@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')


# Пример
logging.basicConfig(level=logging.DEBUG)
add(2, 3)
# Изменение сообщения в лог
add.set_message('Add called')
add(2, 3)

# Изменение уровня логирования
add.set_level(logging.WARNING)
add(2, 3)
