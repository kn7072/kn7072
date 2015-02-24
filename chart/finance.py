import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo, candlestick, fetch_historical_yahoo
from numpy import arange
from pylab import figure, show
from scipy import integrate
import datetime
import csv
import matplotlib.mlab as mlab
import matplotlib
import numpy as np

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
v = 0.1
rate = 0.05/100
t = 360/365
s = 66
k = 66
def black_skoles(x):
    return  (1 / (np.sqrt(2*np.pi)) ) * np.exp(-(x**2)/2)


t_last = r.date[-1]
price_0 = r.adj_close[0]
time_ = []
def d1(price, date):
    t = (t_last - date).days/365
    if t==0: t = 0.0000001
    time_.append(t)
    return (np.log(price/k) + (rate + (v*v)/2)*t) / (v*np.sqrt(t))

def N1(d1):
    return  integrate.quad(black_skoles, -np.inf, d1)[0]

report = r'repote.csv'
report_csv = r'csv_repote.csv'
def delta_strategy(): #price, date
    temp_d1 = [d1(array.adj_close, array.date) for array in r ]
    temp_N_d1 = [N1(d1) for d1 in temp_d1]
    r_ = [list(x) for x in r]
    count = len(r)
    temp_return = []
    for i in range(count):
        tem = list(r[i])
        tem.extend([time_[i]])
        tem.extend([temp_d1[i]])
        tem.extend([temp_N_d1[i]])
        temp_return.append(tem)
    zip_ = list(zip(r_, temp_d1, temp_N_d1))
    zip_2 = []
    write_list = ["\n{0};{1}".format(x[0], x[1]) for x in zip_]
    write_list_simple = [list(x) for x in zip_]
    # with open(report, encoding='utf-8', mode='w') as f:
    #     f.write('xxx')
    with open(report_csv, encoding='utf-8', mode='w') as f1:
        w = csv.writer(f1, delimiter = ';')
        w.writerows(temp_return)  # write_list_simple
    return temp_N_d1
if len(quotes) == 0:
    raise SystemExit

fillcolor = 'darkgoldenrod'
delta = delta_strategy()
t = arange(0.0, 1.0, 0.01)
#fig, ax = plt.subplots()
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(r.date, delta, '-', color=fillcolor)  # sin(2*pi*t)
ax1.grid(True)
#ax1.set_ylim( (-2,2) )
ax1.set_ylabel('delta')
ax1.set_title('time')

for label in ax1.get_xticklabels():
    label.set_color('r')

ax = fig.add_subplot(212)
#fig.subplots_adjust(bottom=0.2)
# ax.xaxis.set_major_locator(mondays)
# ax.xaxis.set_minor_locator(alldays)
ax.xaxis.set_major_formatter(weekFormatter)
#ax.xaxis.set_minor_formatter(dayFormatter)
dx = 10
#quotes_2 = [(x[0], x[1]-10, x[2]-10, x[3]-10, x[4]-10, x[5]-10) for x in quotes]
#plot_day_summary(ax, quotes, ticksize=3)
candlestick(ax, quotes, width=0.6)#
#candlestick(ax, quotes_2, width=0.6)

ax.xaxis_date()
ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

plt.show()