# coding: utf-8
"""Отладочный модуль."""
from inspect import getgeneratorstate


"""
Важно понимать, что выполнение сопрограммы приостанавливается именно по
достижении ключевого слова yield – не раньше и не позже. Выше уже отмечалось,
что код в правой части выражения присваивания вычисляется до выполнения присваивания.
Это означает, что в строке вида b = yield a значение b будет установ-
лено только после активации сопрограммы из клиентского кода. Чтобы осознать
этот факт, требуется некоторое усилие, но его понимание абсолютно необходимо
для осмысленного использования yield в асинхронном программировании
"""


def test_yield() -> None:
    """Отладочная функция."""
    index_iteration = 0
    while True:
        try:
            data_0 = yield index_iteration + 1
            print(f"data_0 = {data_0}")

            data_1 = yield index_iteration + 3
            print(f"data_1 = {data_1}")
            index_iteration += 1
        except StopIteration:
            break


if __name__ == "__main__":
    generator = test_yield()
    res0 = next(generator)
    print(getgeneratorstate(generator))
    res1 = generator.send("A")
    res2 = generator.send("B")
    generator.throw(StopIteration)  #  ZeroDivisionError

    print(getgeneratorstate(generator))
    print()
