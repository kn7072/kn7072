# -*- coding: utf-8 -*-
#--------------------------------------------------------------------
# Данный скрипт предназначеня для создания графиков трендов
# тестов производительности в Jenkins.
#--------------------------------------------------------------------

from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np
import sys
from datetime import datetime

#Задаём шрифт для обходра проблемы отображения кириллических символов
font = {'family': 'Verdana',
        'weight': 'normal'}
rc('font', **font)

#Создаём нужные списки из файла с результатами
file = open(sys.argv[1])
lines = file.readlines()
labels = [x.split(';')[0][:9] for x in lines]
mlabels = []
for n, label in enumerate(labels):
    if n%3 == 0:
        mlabels.append(datetime.strptime(label, '%y/%m/%d ').strftime('%d/%m/%y'))
    else:
        mlabels.append('')
labels = mlabels
medians = [x.split(';')[1] for x in lines]
int_medians = [int(float(x)) for x in medians]
mins = [x.split(';')[2] for x in lines]
int_mins = [int(float(x)) for x in mins]
maxs = [x.split(';')[3] for x in lines]
int_maxs = [int(float(x)) for x in maxs]
x = list(range(1, len(labels) + 1))

#Рисуем диапазоны, в которых колебались значения
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.fill_between(x, int_mins, int_maxs, facecolor='red', alpha=.25)

#Настравиаем вывод графика
plt.grid()
plt.xlabel('Сборки')
plt.ylabel('Время (мс)')
plt.title(sys.argv[2])
plt.xlim(1, len(medians))
plt.ylim(0, max(int_medians + int_maxs) + 1000)
plt.xticks(np.arange(1, len(medians) + 1, 1.0))
plt.margins(0.2)
plt.subplots_adjust(bottom=0.35)
plt.xticks(x, labels, rotation=55)


plt.plot(x, medians, 'b', x, medians, 'o')
plt.savefig(sys.argv[1][:-4] + '.png')
