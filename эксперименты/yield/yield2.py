class BinaryTree:
    def __init__(self, left=None, us=None, right=None):
        self.left = left
        self.us = us
        self.right = right

    def __iter__(self):
        if self.left:
            print("hallo++++")  # выполняется один раз
            w = yield from self.left  # делегирование функции генератору
            print(w+3)  # не выполняется ни разу
        if self.us:
            yield self.us
        if self.right:
            yield from self.right


def yielder():
    while 1:
        a = yield 'a'
        if a is None:
            return 10
        print(a)


def simpl_finc():
    print()


a = BinaryTree(yielder(), yielder(), yielder())
b = iter(a)
#for x in range(5):

next(b)
b.send(7)
b.send(6)
next(b)

#/////////////////////
y = yielder()
s = simpl_finc()
next(y)
y.gi_frame
y.gi_code
y.gi_frame.f_lasti
print()