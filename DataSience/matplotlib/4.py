import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import numpy as np

# стр 75
# Таблица 4.1 — Свойства класса Line2D

x = [1, 5, 10, 15, 20]
y1 = [1, 7, 3, 5, 11]
y2 = [4, 3, 1, 8, 12]
plt.figure(figsize=(12, 7))
plt.plot(x, y1, 'o-r', alpha=0.7, label='first', lw=5, mec='b', mew=2, ms=10)
plt.plot(x, y2, 'v-.g', label='second', mec='r', lw=2, mew=2, ms=12)
plt.legend()
plt.grid(True)
plt.show()

# 4.1.2 Заливка области между графиком и осью
x = np.arange(0.0, 5, 0.01)
y = np.cos(x*np.pi)
plt.plot(x, y, c='r')
# plt.fill_between(x, y)
# plt.fill_between(x, y, where=(y > 0.75) | (y < -0.75))
# plt.fill_between(x, y, where = (y > 0))
# plt.fill_between(x, y, 1)
plt.fill_between(x, 0.5, y, where=y>=0.5)
plt.show()


# Вариант двухцветной заливки:
plt.plot(x, y, c='r')
plt.grid()
plt.fill_between(x, y, where=y>=0, color='g', alpha=0.3)
plt.fill_between(x, y, where=y<=0, color='r', alpha=0.3)
plt.show()

# 4.1.3 Настройка маркировки графиков
x = [1, 2, 3, 4, 5, 6, 7]
y = [7, 6, 5, 4, 5, 6, 7]
plt.plot(x, y, marker='o', c='g')
plt.show()

x = np.arange(0.0, 5, 0.01)
y = np.cos(x*np.pi)
plt.plot(x, y, marker='o', c='g')
plt.show()




