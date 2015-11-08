import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo, candlestick, fetch_historical_yahoo
from scipy.optimize import minimize_scalar, basinhopping
from scipy import integrate
import datetime
import csv
import matplotlib.mlab as mlab
import matplotlib
import numpy as np
from scipy.optimize import fsolve

# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
date1 = (2004, 2, 1)
date2 = (2004, 4, 12)
mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
alldays = DayLocator()              # minor ticks on the days
weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
dayFormatter = DateFormatter('%d')      # e.g., 12
startdate = datetime.date(2013,4,1)
today = enddate = datetime.date(2013,12,13)#datetime.date.today()
matplotlib.dates.date2num(today)
ticker = 'QQQ'
#quotes = quotes_historical_yahoo(ticker, startdate, enddate)#fetch_historical_yahoo    quotes_historical_yahoo
# a numpy record array with fields: date, open, high, low, close, volume, adj_close)
fh = fetch_historical_yahoo(ticker, startdate, enddate)
r = mlab.csv2rec(fh); fh.close()
r.sort()
#quotes = quotes_historical_yahoo('INTC', date1, date2)

quotes = [(matplotlib.dates.date2num(x[0]), x[1], x[2], x[3], x[4], x[5]) for x in r]
v = 0.1207 #  0.2258 # 0.2472
k = 206
rate = 0.025/100
t0 = 72 #217-60 360/365 146
t1 = datetime.datetime(2014,2,24) # 2012,11,16
t2 = datetime.datetime(2015,2,2)  # 2013,6,21

price = 1.12  # 77.78

def future_levels(begin_data, days_step):
    """принимает дату начала и интервал в днях"""

    global t1, t2, t0
    t0 = days_step
    days = datetime.timedelta(days=days_step)
    t1 = begin_data
    t2 = t1 + days

def black_skoles(x):
    return  (1 / (np.sqrt(2*np.pi)) ) * np.exp(-(x**2)/2)

def gamma(d1, t=None):
    if t is None : t = t0/365
    g = black_skoles(d1)/(k*v*np.sqrt(t))
    return g

def d1(price, t=None):  # , date
    if t is None : t = t0/365
    return (np.log(price/k) + (rate + (v*v)/2)*t) / (v*np.sqrt(t))

def N1(d1):
    return  integrate.quad(black_skoles, -np.inf, d1)[0]

def delta_gamma(stack_size, t=None, n = 0): #, price
    return lambda x: (N1(d1(x,t))*100 + n*gamma(d1(x,t), t) - stack_size)  # 10/((gamma(d1(x)))**3)  10*gamma(d1(x))

def fsolve_reh(stack_size, t=None):
    return fsolve(delta_gamma(stack_size, t), k)

def delta(price):
    d1_temp = d1(price)
    return  integrate.quad(black_skoles, -np.inf, d1_temp)[0]

def price_option(price, t=None):
    if t is None : t = t0/365
    d1_temp = d1(price)
    d2_temp = d1_temp - v*np.sqrt(t)
    N_d1 = integrate.quad(black_skoles, -np.inf, d1_temp)[0]
    N_d2 = integrate.quad(black_skoles, -np.inf, d2_temp)[0]
    c = N_d1*price - N_d2*k*np.exp(-(rate*t))
    print("### price= "+str(c)+" ###")
    return c

#k = price = 92.39
#x = N1(d1(price))*100 + 10/((100*gamma(d1(price)))**3)
# stack_size = 30,7
# y = fsolve(delta_gamma(stack_size), k)
future_levels(datetime.datetime(2015,3,9), 33)
list_rehedg = [x*10 for x in range(11)]
list_rehedg[0] = 1
list_rehedg[-1] = 99
price_list = [(delta, fsolve_reh(delta)) for delta in list_rehedg]
delta_for_h = [[delta_, round(delta(price[0])*100,3), price[0]] for delta_, price  in price_list]
sting_for_txt_delta_gamma = ["%d  %.3f  %.4f\n" % (x[0], x[1], x[2]) for x in delta_for_h]  # для записи в txt
string_for_csv = [[str(delta_), str(round(delta(price[0])*100,3)), '%.4f' % price[0]] for delta_, price  in price_list]  # для csv

for x in sting_for_txt_delta_gamma:
    print(x)

# иницаализация - дата начала и интервал дней вперед
xx = 205.82
g = gamma(d1(xx))
c = price_option(xx)  # k
# d1_ = d1(1.1279)
# g = gamma(d1_)
print(delta(xx))
data = [
         ['Blues','Elwood','1060 W Addison','Chicago','IL','60613'],
         ['McGurn','Jack', '4802 N Broadway', 'Chicago', 'IL', '60640']
       ]

delta_gamma_levels_csv = r'delta_gamma_levels.csv'
n = 3
with open(delta_gamma_levels_csv, encoding='utf-8', mode='w') as f1:
    w = csv.writer(f1, delimiter = ';', lineterminator='\n')
    delta_days = (t2 - t1).days
    massage = [['Дата начала %s' % t1.strftime('%d.%m.%Y')], ['дата конца %s' % t2.strftime('%d.%m.%Y')],
               ['Всего календарных дней = %d' % delta_days]]
    w.writerows(massage)
    # делим полученный интервал на n периодов
    # будем двигать время вперед на n дней
    step_day = int(delta_days / n)
    for step in range(n+1):
        day = datetime.timedelta(days=step*step_day)
        data_n = t1 + day
        print(data_n.strftime('%d.%m.%Y'))
        w.writerow([data_n.strftime('%d.%m.%Y')])
        # осталось дней до экспереции
        t_n = delta_days - step*step_day
        if t_n == 0:
            t_n = 0.1
        # тоже только выраженное в годах
        t_n_yar = t_n / 365
        price_list = [(delta, fsolve_reh(delta, t_n_yar)) for delta in list_rehedg]
        string_for_csv = [[str(delta_), str(round(delta(price[0])*100,3)), '%.4f' % price[0]] for delta_, price  in price_list]  # для csv
        w.writerows(string_for_csv)
        w.writerow(["######"])

# delta_gamma_levels_csv = r'delta_gamma_levels.csv'
# with open(delta_gamma_levels_csv, encoding='utf-8', mode='w') as f1:
#     f1.write(t3.strftime('%d.%m.%Y'))
#     f1.writelines(sting_delta_gamma)

t_last = r.date[-1]
price_0 = r.adj_close[0]
time_ = []
report = r'repote.csv'
report_csv = r'csv_repote.csv'
def delta_strategy(): #price, date
    temp_d1 = [d1(array.adj_close, array.date) for array in r ]
    temp_N_d1 = [N1(d1) for d1 in temp_d1]
    # r_ = [list(x) for x in r]
    # count = len(r)
    # temp_return = []
    # for i in range(count):
    #     tem = list(r[i])
    #     tem.extend([time_[i]])
    #     tem.extend([temp_d1[i]])
    #     tem.extend([temp_N_d1[i]])
    #     temp_return.append(tem)
    # zip_ = list(zip( temp_d1, temp_N_d1))  #  r_,
    # zip_2 = []
    # write_list = ["\n{0};{1}".format(x[0], x[1]) for x in zip_]
    # write_list_simple = [list(x) for x in zip_]
    # # with open(report, encoding='utf-8', mode='w') as f:
    # #     f.write('xxx')
    # with open(report_csv, encoding='utf-8', mode='w') as f1:
    #     w = csv.writer(f1, delimiter = ';')
    #     w.writerows(temp_return)  # write_list_simple
    return temp_N_d1