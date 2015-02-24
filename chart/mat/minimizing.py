from scipy.optimize import minimize_scalar, basinhopping
import numpy as np

def f(x):
    return x**2 + 2*x + 1 #(x - 2) * x * (x + 2)**2

res = minimize_scalar(f)
res.x

func = lambda x: np.cos(14.5 * x - 0.3) + (x + 0.2) * x
x0=[3.]
minimizer_kwargs = {"method": "BFGS"}
ret = basinhopping(func, x0, minimizer_kwargs=minimizer_kwargs, niter=200)
print("global minimum: x = %.4f, f(x0) = %.4f" % (ret.x, ret.fun))

from scipy.optimize import fsolve
import math

def equations(p):
    x, y = p
    return (x+y**2-4, math.exp(x) + x*y - 3)

x, y =  fsolve(equations, (1, 1))
print (equations((x, y)))
