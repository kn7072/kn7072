# coding:utf-8


class A:

    A_a = 10
    A_b = "a"

    def __init__(self, a=1) -> None:
        
        self.a = a
        # self.x = a ** 2
        # pass

    def method_a(self):
        print(self.A_a)
