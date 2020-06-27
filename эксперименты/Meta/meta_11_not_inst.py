#  https://habr.com/ru/company/binarydistrict/blog/422415/
class FinalMeta(type):

    def __new__(mcs, name, bases, attrs):
        for cls in bases:
            if isinstance(cls, FinalMeta):
                raise TypeError(f"Can't inherit {name} class from final {cls.__name__}")

        return super().__new__(mcs, name, bases, attrs)


class A(metaclass=FinalMeta):
    """От меня нельзя наследоваться!"""
    pass


class B(A):
    x = 10
    pass

# TypeError: Can't inherit B class from final A
# Ну я же говорил!