# -*- coding: utf-8 -*-

# import atf
# from atf.helper import wait
import unittest
from datetime import datetime
import time
import sys
# import string
# from pages.test_online.login import LoginPage
# from pages.test_online.main import MainPage
# from pages.test_online.kontragents.main import KontragentMainPage
# from pages.test_online.documents.index import DocsPage
# from pages.test_online.reports.fns import ReportsFNS
from matplotlib import numpy as np
# from pages.test_online.kontragents import main
# from pages.test_online.kontragents import card
from selenium import webdriver
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter , HourLocator, DayLocator
import matplotlib.dates as dates_mt
from matplotlib.dates  import YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange
from draw_graph import graph

def performance(name, count=2):
    """Реализует декоратор для измерения времени отработки кода тестового метода"""
    def decorator(f):

        def wrapper(*args):
            results = []
            with open('./templates/sampler.template', 'r', encoding='utf-8') as file:
                sampler = file.read()
            # число неудавшихся измерений
            failure = 0
            name_test = r"./report/" + args[0]._testMethodName + ".txt"#.csv

            for i in range(count):
                results_file = open('results.jtl', 'a', encoding='utf-8')
                time.sleep(2)
                start_time =  time.time()# datetime.now()
                success = True
                try:
                    f(*args)
                    # label_time -имя метки например labeltime1
                    # time_and_text[0] - это время которое прошло до метки
                    # time_and_text[1]- это коментарий для легенды на графике
                    label = [(label_time,time_and_text[0],time_and_text[1]) for label_time, time_and_text in args[0].__dict__.items() if label_time.startswith('labeltime')]
                    count_label = len(label)
                    if label:
                        # https://wiki.python.org/moin/HowTo/Sorting
                        label = sorted(label, key = lambda tupl_ :tupl_[1])  # отсортировали по времени
                        legend_text = [text[2] for text in label]
                        legend_text.append("the end")
                        # добавим в конец списка легенды одно значение для указания завершения теста
                except Exception as e:
                    success = False
                if success:
                    finish_time = time.time()
                    duration = [label_time[1]-start_time for label_time in label]
                    duration.append(finish_time - start_time)
                    sampler_success = 'true'
                    print(duration)
                else:
                    duration = 1000
                    sampler_success = 'false'
                    failure += 1
                results.append(duration)
            # разделяем списки(транспонируем)
            res = []
            for i in range(count_label):  # todo подумать над тем если меток нет
                x = [n[i] for n in results ]
                res.append(x)
            # считаем средние значения
            res_avg = [str(np.average(avg)) for avg in res]
            # print("++++++++")
            # print(res_avg)
            dt = datetime.strftime(datetime.now(), '%y/%m/%d %H:%M:%S')
            if failure*100/count < 3:
                file = open(name + '_trends.csv', 'a', encoding='utf-8')
                # формируем строку для записи
                strig = '\n'+dt+";"+";".join(res_avg)
                file.write(strig)#'\n{0};{1};{2};{3}'.format(dt, str(np.average(results))))  # str(np.median(results)), min(results), max(results))
                file.close()
                graph(legend_text)
            else:
                with open(name_test, 'a', encoding="utf-8") as report:
                    report.write('\n{0};{1};{2};{3};{4}'.format(dt, 0, 0, 0, 0))
        return wrapper
    return decorator

def graf():
    # plt.rc('axes', grid=True)
    # plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)

    # fig = plt.figure(facecolor='white')
    # textsize = 9
    # left, width = 0.1, 0.8
    # rect1 = [left, 0.7, width, 0.2]
    # axescolor  = '#f6f6f6'  # the axes background color
    fig, ax = plt.subplots()

    # fig, ax = plt.subplots()
    fillcolor = 'darkgoldenrod'
    monthsFmt = DateFormatter("%d %b %y %H:%M:%S")
    with open(r".\report\test_online_main_page.csv", 'r', encoding='utf-8') as f:
        arr = [x.strip().split(';') for x in f]
        arr_time = [datetime.strptime(x[0], '%y/%m/%d %H:%M:%S') for x in arr[1:]]
        arr_value = [x[1] for x in arr[1:]]
    #datetime.strptime("14/07/05 10:20:16", '%y/%m/%d %H:%M:%S')  # 05.06.2011 "%d.%m.%Y"
    dt = datetime.now()
    vv = dates_mt.date2num(dt)
    date = []
    n = []
    # plt.plot(arr_time, arr_value, color=fillcolor)

    #ax.xaxis.set_minor_locator(mondays)
    rule = rrulewrapper(YEARLY, byeaster=1, interval=1)
    loc = RRuleLocator(rule)
    ax.plot_date(arr_time, arr_value, '-')#
    #ax.xaxis.set_major_formatter(monthsFmt)
    #fig.add_subplot(111)
    #ax.xaxis.set_major_locator(loc)
    hour = HourLocator(range(1,25), interval=4)
    formatter = DateFormatter('%H:%M:%S %m/%d/%y')
    ax.xaxis.set_major_locator(hour)
    ax.xaxis.set_major_formatter(formatter)
    ##############################################
    fig, ax2 = fig.add_subplot()
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    sizes = [15, 30, 45, 10]
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
    explode = (0, 0.1, 0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')

    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
    # Set aspect ratio to be equal so that pie is drawn as a circle.
    plt.axis('equal')


    plt.savefig("fname2.png", dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)
    plt.show()

def graf2():
    arr_time = list()
    arr_value = list()
    wins = list()
    plt.rc('axes', grid=True)
    #plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    fillcolor = 'darkgoldenrod'
    monthsFmt = DateFormatter("%d %b %y %H:%M:%S")
    with open(r".\report\test_online_main_page.txt", 'r', encoding='utf-8') as f:
        arr = [x.strip().split(';') for x in f]
        count = len(arr)
        for x in arr:
                #if x[4]=='1':
                # arr_time = [datetime.strptime(x[0], '%y/%m/%d %H:%M:%S') for x in arr[1:]]
                # arr_value = [x[1] for x in arr[1:]]
                arr_time.append(datetime.strptime(x[0], '%y/%m/%d %H:%M:%S').strftime('%d/%m/%y'))  # '%y/%m/%d %H:%M:%S'
                arr_value.append(x[1])
                #wins.append(1)
    x = list(range(1, len(arr_time) + 1))
    plt.grid()
    plt.xlabel('Сборки')
    plt.ylabel('Время (мс)')
    plt.xticks(np.arange(1, len(arr_value) + 1, 1.0))
    plt.margins(0.2)
    plt.subplots_adjust(bottom=0.35)
    plt.xticks(x, arr_time, rotation=55)
    fig, ax = plt.subplots()
    #ax.stackplot(x, y1, y2, y3)
    plt.plot(x, arr_value, 'b', x, arr_value, 'o')#
    plt.show()

    fig = plt.figure(facecolor='white')
    #fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')
    ax = fig.add_subplot(121)
    plt.title(r'$\sin(x)$')
    # ax.plot_date(arr_time, arr_value, 'o-')
    plt.xticks(range(1, len(arr_value)),arr_time, rotation=45)  # 'vertical'
    plt.plot(arr_time,arr_value, 'o')
    # plt.xlabel(r"$time$", fontsize=14)
    # plt.ylabel(r"$timetest$", fontsize=14)
    #plt.setp(arr_time, rotation=45, fontsize=8)
    # hour = HourLocator(range(1,25), interval=4)
    # day = DayLocator(range(1,32), interval=1)
    # formatter = DateFormatter('%m/%d/%y')#:%S%H:%M
    # ax.xaxis.set_major_locator(day)
    # ax.xaxis.set_major_formatter(formatter)

    # labels = 'Wins', 'Los'
    # wins_ = wins
    # sizes = [15, 30]#, 45, 10
    # colors = ['yellowgreen', 'gold']  #, 'lightskyblue', 'lightcoral'
    # explode = (0.1, 0.1) #, 0.1, 0.1 only "explode" the 2nd slice (i.e. 'Hogs')
    #
    # ax2 = fig.add_subplot(122)
    # ax2.pie(sizes, explode=explode, labels=labels, colors=colors,
    #     autopct='%1.1f%%', shadow=True, startangle=90)


    # plt.title(r'$\cos(x)$')
    # ax2.plot_date(arr_time, arr_value)
    # hour = HourLocator(range(1,25), interval=4)
    # formatter = DateFormatter('%m/%d/%y')#%H:%M:%S
    # ax2.xaxis.set_major_locator(hour)
    # ax2.xaxis.set_major_formatter(formatter)

    plt.show()


class Perfomans(unittest.TestCase):

    def setUp(self):
        print("setUp")
    def tearDown(self):
        #graf()
        print("tearDown")

    @performance("MainPage")
    def test_online_main_page(self):
        """Тест на время открытия разводящей страницы"""

        setattr(self, 'labeltime0', [time.time(), "делай раз"])
        labeltime0 = time.time()
        driver = webdriver.Firefox()
        driver.get("http://www.google.ru")
        time.sleep(1)
        labeltime1 = time.time()
        setattr(self, 'labeltime1', [time.time(), "делай два"])
        print(time.time())
        time.sleep(1)
        labeltime2 = time.time()
        setattr(self, 'labeltime2', [time.time(), "делай три"])
        driver.quit()


if __name__ == '__main__':
    unittest.main()
#graf2()
# test_online_main_page()
#print()