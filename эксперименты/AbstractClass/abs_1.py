# -*- coding: utf-8 -*-
import abc


# 18.2.7. Абстрактные свойства
class Base(abc.ABC):
    @property
    @abc.abstractmethod
    def value(self):
        return 'Should never reach here'

    @property
    @abc.abstractmethod
    def constant(self):
        return 'Should never reach here'


class Implementation(Base):
    @property
    def value(self):
        return 'concrete property'

    constant = 'set by a class attribute'


try:
    b = Base()
    print('Base.value:', b.value)
except Exception as err:
    print('ERROR:', str(err))

i = Implementation()
print('Implementation.value :', i.value)
print('Implementation.constant:', i.constant)