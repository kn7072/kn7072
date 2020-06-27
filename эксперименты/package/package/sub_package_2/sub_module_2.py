import inspect
v = 1

def y(i=1):
    r = 2

class A:
    pass

class B(A):
    pass

def x(obj=None, instance_class=None):
    a = 5
    locals()
    globals()
    inspect.getargspec(y)  # ArgSpec(args=['i'], varargs=None, keywords=None, defaults=(1,))
    # inspect.getclasstree(B, True)
    inspect.getmodule(obj)
    # inspect.getfile(obj)
    inspect.getsourcefile(obj)  # 'D:/kn7072/эксперименты/package/file.py'
    # inspect.getsourcefile(instance_class) инстанцы не работают
    ####################################################
    inspect.getsource(obj)
    # inspect.getsource(instance_class) инстанцы не работают
    print("sub_module_2")
    inspect.stack()
    current_frame = inspect.currentframe()
    inspect.getargvalues(current_frame)
    current_frame.f_locals  # локально пространство имен
    current_frame.f_globals
    traceback = inspect.getframeinfo(current_frame)  # Traceback(filename='D:/kn7072/эксперименты/package\\package\\sub_package_2\\
                                                                                                     # sub_module_2.py',
                                         #  lineno=29,
                                         #  function='x',
                                         #  code_context=['    inspect.getargvalues(current_frame)\n'],
                                         #  index=0)

    inspect.getinnerframes(traceback)
    frame = inspect.stack()[9][0]