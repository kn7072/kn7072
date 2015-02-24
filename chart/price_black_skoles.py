from scipy import integrate
from scipy.special import jv, jn_zeros
from scipy.integrate import simps
import numpy as np
import math

v = 0.1
r = 0.05/100
t = 0.2137  # 100/365
s = 83.1
k = 83
################################
d1 = (np.log(s/k) + (r + v*v/2)*t) / (v*np.sqrt(t))  # np.log(np.exp(1)) - 1 натуральный логорифм
d2 = d1 - (v*np.sqrt(t))
def black_skoles(x):
    return (1 / (np.sqrt(2*np.pi)) ) * np.exp(-(x**2)/2)

N_d1 = integrate.quad(black_skoles, -np.inf, d1)[0]
N_d2 = integrate.quad(black_skoles, -np.inf, d2)[0]
c = s*N_d1 - (k*N_d2*np.exp(-r*t))
print(N_d1, N_d2, c)
################################
print()
def f1(x):
    return x**2
def integrand(x):  # 12 стр
    return np.exp(-(x**2)/2)
################################
x = np.array([1, 3, 4])
y1 = f1(x)
I1 = integrate.simps(y1, x)
print(I1)
################################
result_1 = integrate.quad(integrand, -np.inf, np.inf) #, args=(1, 1) -np.inf
print(result_1)  # корень из 2 пи - все правильно
result = integrate.quad(lambda x: jv(2.5, x), 0, 4.5)  # lambda x: jv(2.5,x), 0, 4.5
print()
#stats.norm.pdf(x) = exp(-x**2/2)/sqrt(2*pi)