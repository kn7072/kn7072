import inspect
x = 10
w = 55
def fun(y):
    e = 4
    y()
    #  y.__globals__['w']=globals()['w']
    if inspect.isfunction(y):
        print(inspect.getmodule(y))
        y(7)
    else:
        y()