import contextlib
import wrapt


@contextlib.contextmanager
def bold_text(name):
    print('<b>')
    yield  # код из блока with выполнится тут
    print('</b> %s' % name)


@wrapt.decorator
def timing(func, instance, args, kwargs):
    """
    Замеряет время выполнения произвольной фукнции или метода.
    Здесь мы используем библиотеку https://wrapt.readthedocs.io/en/latest/
    чтобы безболезненно декорировать методы класса и статические методы
    """
    with bold_text(func.__name__):
        return func(*args, **kwargs)


@wrapt.decorator
def timing_2(func, instance, args, kwargs):
    """
    Замеряет время выполнения произвольной фукнции или метода.
    Здесь мы используем библиотеку https://wrapt.readthedocs.io/en/latest/
    чтобы безболезненно декорировать методы класса и статические методы
    """
    return func(*args, **kwargs)


@timing
def f():
    print("f")

@timing_2
def f_2():
    print("f")

lambda_x = lambda : print("ffff")
y = timing(lambda_x)
y2 = timing_2(lambda_x)
print()

