import numpy as np

a = np.arange(4).reshape(2, 2)
b = np.arange(6).reshape(3, 1, 2)
print(a)
print(b)

c = b + a
#  Последние оси совпадают по размерам
...  #  b: 3 x 1 x 2
...  #  a:     2 x 2
...  #  c: 3 x 2 x 2
...  #    _----^----_
...  #  предпоследняя ось "b" может быть расширена до 2
print(c, c.shape)