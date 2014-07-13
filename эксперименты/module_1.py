import inspect
x = 10
def fun(y):
    if inspect.isfunction(y):
        print(inspect.getmodule(y))
        y(7)
    else:
        y()