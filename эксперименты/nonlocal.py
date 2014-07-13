#-*- coding: utf-8 -*-
def tester(start):
    state = start  # В каждом вызове сохраняется свое значение state
    def nested(label):
        nonlocal state      # Объект state находится
        print(label, state) # в объемлющей области видимости
        state += 1 # Изменит значение переменной, объявленной как nonlocal
    return nested

F = tester(0)
F('spam')          # Будет увеличивать значение state при каждом вызове
F('ham')
F('eggs')

