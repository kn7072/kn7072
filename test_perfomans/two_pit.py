import numpy as np
import matplotlib.pyplot as plt

Y, X = np.mgrid[-3:3:100j, -3:3:100j]
U = -1 - X**2 + Y
V = 1 + X - Y**2
speed = np.sqrt(U*U + V*V)

# plt.plot([1,2,3])
# plt.ylabel('some numbers')

# plt.streamplot(X, Y, U, V, color=U, linewidth=2, cmap=plt.cm.autumn)
# plt.colorbar()

f, (ax1, ax2) = plt.subplots(ncols=2)
ax1.plot([1,2,3])

labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
explode = (0, 0.1, 0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')

ax2.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
# ax2.plot([1,5,1.9,2])

# f, (ax1, ax2) = plt.subplots(ncols=2)
# ax1.streamplot(X, Y, U, V, density=[0.5, 1])
#
# lw = 5*speed/speed.max()
# ax2.streamplot(X, Y, U, V, density=0.6, color='k', linewidth=lw)

plt.show()