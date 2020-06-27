# -*- encoding:utf-8 -*-
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

x = ["a", "b", "c"]
y = [1, 2, 3]
d1 = dict(t for t in zip(x, y))
d2 = {t[0]: t[1] for t in zip(x, y)}
# Есть словарь. Инвертировать его. Т.е. пары ключ: значение поменять местами — значение: ключ.
d_ivers = {val: key for key, val in d1.items()}
# Есть два кортежа, получить третий как объединение уникальных элементов первых двух кортежей
c = (1, 3, 4, 6)
c2 = (1, 2, 4, 7)
c3 = set(c).union(set(c2))
############################
# Есть два списка разной длины, в одном ключи, в другом значения. Составить словарь. Для ключей, для которых нет
# значений использовать None в качестве значения. Значения, для которых нет ключей игнорировать.
l1 = ["a", "b", "c", "d", "e"]
l2 = [1, 2, 3]
if len(l1) > len(l2):
    diff = len(l1) - len(l2)
    l2.extend([None]*diff)
d7 = dict(t for t in zip(l1, l2))
############################
x, y = np.mgrid[-1:1:20j, -1:1:20j]
z = (x+y) * np.exp(-6.0*(x*x+y*y))
plt.figure()
plt.pcolor(x, y, z)
plt.colorbar()
plt.title("Sparsely sampled function.")
plt.show()

xnew, ynew = np.mgrid[-1:1:70j, -1:1:70j]
tck = interpolate.bisplrep(x, y, z, s=0)
znew = interpolate.bisplev(xnew[:, 0], ynew[0, :], tck)
plt.figure()
plt.pcolor(xnew, ynew, znew)
plt.colorbar()
plt.title("Interpolated function.")
plt.show()
