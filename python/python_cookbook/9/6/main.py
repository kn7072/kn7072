# coding: utf-8

# 9.6. Определение декоратора, принимающего необязательный аргумент

from functools import partial, wraps
import logging


def logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    if func is None:
        return partial(logged, level=level, name=name, message=message)

    logname = name if name else func.__module__
    log = logging.getLogger(logname)
    logmsg = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        log.log(level, logmsg)
        return func(*args, **kwargs)

    return wrapper


# Пример использования
@logged
def add(x, y):
    return x + y

"""
def add(x, y):
    return x + y
add = logged(add)

"""


#########################################################
@logged(level=logging.CRITICAL, name="example")
def spam():
    print('Spam!')

"""
def spam():
    print('Spam!')
spam = logged(level=logging.CRITICAL, name='example')(spam)

"""