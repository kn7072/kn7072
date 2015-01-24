import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime

fnx = lambda : np.random.randint(5, 50, 10)
y = np.row_stack((fnx(), fnx(), fnx()))
x = np.arange(10)
arr_time = list()
arr_value = list()
wins = list()
plt.rc('axes', grid=True)
with open(r"d:\git_hub_new\kn7072\test_perfomans\report\test_online_main_page.txt", 'r', encoding='utf-8') as f:
        arr = [x.strip().split(';') for x in f]
        count = len(arr)
        for x in arr:
                #if x[4]=='1':
                # arr_time = [datetime.strptime(x[0], '%y/%m/%d %H:%M:%S') for x in arr[1:]]
                # arr_value = [x[1] for x in arr[1:]]
                arr_time.append(datetime.strptime(x[0], '%y/%m/%d %H:%M:%S').strftime('%d/%m/%y'))  # '%y/%m/%d %H:%M:%S'
                arr_value.append(x[1])
                #wins.append(1)

y1, y2, y3 = fnx(), fnx(), fnx()
n = list(range(1, len(arr_time) + 1))
plt.xticks(n, arr_time, rotation=55)


fig, ax = plt.subplots()
ax.stackplot(n, n, n)

plt.show()

X = np.arange(0,10,1)
Y = X + 5*np.random.random((5,X.size))

baseline = ["zero", "sym", "wiggle", "weighted_wiggle"]
for n,v in enumerate(baseline):
    plt.subplot(2,2,n+1)
    plt.stackplot(X,*Y,baseline=v)
    plt.title(v)
    plt.axis('tight')
plt.show()