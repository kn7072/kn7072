import inspect
x = 10
def fun(y):
    e = 4
    if inspect.isfunction(y):
        print(inspect.getmodule(y))
        y(7)
    else:
        y()