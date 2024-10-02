a = 5

def print_a():
    print(a)

def change_a(x):
    global a
    a = x

def add_c():
    from c import const
