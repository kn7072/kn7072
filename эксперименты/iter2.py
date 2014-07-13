class BinaryTree:
    def __init__(self, left=None, us=None, right=None):
        self.left = left
        self.us = us
        self.right = right

    def __iter__(self):
        if self.left:
            yield from self.left
        if self.us:
            yield self.us
        if self.right:
            yield from self.right


def yielder():
    while 1:
        a = yield 'a'
        print (a)

a=BinaryTree(yielder(), yielder(), yielder())
print()
b=iter(a)  # generator object
next(b)
next(b)
next(b)
b.send(3)