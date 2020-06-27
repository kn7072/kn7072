def fun():
    a = "x"
g = dir(fun)

def fun_child():
    print("fun_child")
fun.__dict__['child'] = fun_child

fun.b = 5
g2 = dir(fun)
fun.child()
fun.__code__
print()