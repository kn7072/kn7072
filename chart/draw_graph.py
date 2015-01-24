# -*- coding: utf-8 -*-
from matplotlib import rc
import matplotlib.pyplot as plt
import time
import numpy as np
import sys
from datetime import datetime
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter , HourLocator, DayLocator

def graph(legend=None, path_to_file=None):
    #Задаём шрифт для обхора проблемы отображения кириллических символов
    font = {'family': 'Verdana', 'weight': 'normal'}
    rc('font', **font)

    arr_time = list()
    arr_value = list()
    wins = list()
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    fillcolor = 'darkgoldenrod'
    monthsFmt = DateFormatter("%d %b %y %H:%M:%S")
    time_label = []
    x = []
    def fun(array):
        count = len(array)
        count_x = len(x)
        if count > count_x:
            for i in range(count-count_x):
                x.append([])
        for i in range(count):
            x[i].append(array[i])
        return array[0]

    with open(path_to_file, 'r', encoding='utf-8') as f:  #r"d:\git_hub_new\kn7072\test_perfomans\MainPage_trends.csv" d:\KontragentsPage_trends.csv
        arr = [fun(x.strip().split(';')) for x in f]
        count = len(arr)
        for t in arr:
            arr_time.append(datetime.strptime(t, '%y/%m/%d %H:%M:%S'))  # .strftime('%d/%m/%y')
    fig = plt.figure(facecolor='white', figsize=(13, 10))
    plt.xlabel('Сборки')
    plt.ylabel('Время (с)')
    fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')
    ax = fig.add_subplot(111)
    plt.gca().xaxis.set_major_formatter(DateFormatter('%d/%m/%y'))
    #plt.gca().xaxis.set_major_locator(DayLocator())
    color = ['r', 'g', 'y', 'm', 'b', 'c', 'k']
    if legend:
        for i in reversed(range(len(x)-1)):  # -1 чтобы не учитывать первый столбец - дата
            plt.plot(arr_time, x[i+1], label=legend[i], marker='.', linestyle="-", color=color[i]) #
        legend.reverse()
        plt.legend(loc='upper center', markerscale=2, bbox_to_anchor=(0.5, -0.12), ncol=1, fancybox=True, shadow=True, prop={'size':10})
        #plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=1, fancybox=True, shadow=True, prop={'size':10})
    else:
        for i in range(len(x)-1):  # -1 чтобы не учитывать первый столбец - дата
            plt.plot(arr_time, x[i+1], marker='.', linestyle="-", color=color[i])
    plt.gcf().autofmt_xdate()
    #plt.show()
    plt.savefig(path_to_file[:-4] + '.png')
    #plt.savefig(r"D:/СКРИНЫ ДЛЯ ОТЛАДКИ ЛЕГЕНДЫ/"+str(time.time()) + '.png')

if __name__ == "__main__":
    path_file = sys.argv[1]
    graph(path_file=path_file)
