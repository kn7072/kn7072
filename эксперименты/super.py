class Root:
    def draw(self):
        print("ss")
        pass            # переданная цепь останавливается здесь

class Shape(Root):
    def __init__(self, **kwds):
        self.shapename = kwds.pop('shapename')
        super().__init__(**kwds)
    def draw(self):
        print('Drawing.  Setting shape to:', self.shapename)
        super().draw()

class ColoredShape(Shape):
    def __init__(self, **kwds):
        self.color = kwds.pop('color')
        super(ColoredShape,self).__init__(**kwds)
    def draw(self):
        print('Drawing.  Setting color to:', self.color)
        super().draw()

cs = ColoredShape(color='blue', shapename='square')
cs.draw()