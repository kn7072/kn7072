import matplotlib.pyplot as plt
import numpy as np

plt.plot([1, 2, 3, 4, 5], [1, 2, 3, 4, 5])
# plt.show()

# 1.3 Построение графика
x = np.linspace(0, 10, 50)
y = x
plt.title('Линейная зависимость y = x') # заголовок
plt.xlabel('x')  # ось абсцисс
plt.ylabel('y')  # ось ординат
plt.grid()  # включение отображения сетки
plt.plot(x, y)  # построение графика
plt.plot(x, y + 1, 'r--')  # построение графика
# plt.show()

# 1.4 Несколько графиков на одном поле
x = np.linspace(0, 10, 50)
y1 = x
# Квадратичная зависимость
y2 = [i**2 for i in x]
# Построение графика
plt.title('Зависимости: y1 = x, y2 = x^2')  # заголовок
plt.xlabel('x')  # ось абсцисс
plt.ylabel('y1, y2')  # ось ординат
plt.grid()  # включение отображения сетки
plt.plot(x, y1, x, y2)  # построение графика
# plt.show()

# 1.5 Представление графиков на разных полях
x = np.linspace(0, 10, 50)
y1 = x  # Линейная зависимость
y2 = [i**2 for i in x]  # Квадратичная зависимость
# Построение графиков
plt.figure(figsize=(9, 9))
plt.subplot(2, 1, 1)
"""
первый аргумент — количество строк, 
второй — столбцов в формируемом поле,
третий — индекс (номер поля, считаем сверху вниз, слева направо).
"""
plt.plot(x, y1)  # построение графика
plt.title('Зависимости: y1 = x, y2 = x^2')  # заголовок
plt.ylabel('y1', fontsize=14)  # ось ординат
plt.grid(True)  # включение отображение сетки
plt.subplot(2, 1, 2)
plt.plot(x, y2)  # построение графика
plt.xlabel('x', fontsize=14)  # ось абсцисс
plt.ylabel('y2', fontsize=14)  # ось ординат
plt.grid(True)  # включение отображение сетки
plt.show()

# 1.6 Построение диаграммы для категориальных данных
fruits = ['apple', 'peach', 'orange', 'bannana', 'melon']
counts = [34, 25, 43, 31, 17]
plt.bar(fruits, counts)
plt.title('Fruits!')
plt.xlabel('Fruit')
plt.ylabel('Count')
plt.show()

# 1.7 Основные элементы графика