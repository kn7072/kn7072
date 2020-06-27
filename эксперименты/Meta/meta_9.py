# https://habr.com/ru/company/binarydistrict/blog/422409/


class MetaRow(type):
    # глобальный счетчик всех созданных рядов
    row_count = 0
    row_count_2 = 0

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)

        # Кэшируем список всех полей в ряду отсортированный по алфавиту
        cls.__header__ = ['№'] + sorted(attrs['__annotations__'].keys())
        return cls

    def __call__(cls, *args, **kwargs):
        print("__call__")
        # создание нового ряда происходит здесь
        row: Row = super().__call__(*args, **kwargs)
        # увеличиваем глобальный счетчик
        cls.row_count += 1
        cls.row_count_2 += 1

        # выставляем номер текущего ряда
        row.counter = cls.row_count
        return row


class Row(metaclass=MetaRow):
    name: str
    age: int
    x = 5

    def __init__(self, **kwargs):
        self.counter = None
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __str__(self):
        out = [self.counter]

        # аттрибут __header__ будет динамически добавлен в метаклассе
        for name in self.__header__[1:]:
            out.append(getattr(self, name, 'N/A'))
        return ' | '.join(map(str, out))


row = Row(a=5)
row_2 = Row(a=6)
row_3 = Row(a=7)
print()

