from nose.tools import assert_raises

class Foo:
    def exist(self):
        return True
    def get(self):
        raise IOError('access denied')
    def calc(self, v):
        return 2*v

class TestFoo:
    def setUp(self):
        self.multiplier = 2
    def teardown(self):
        pass
    def test_exist(self):
        f = Foo()
        assert f.exist() == True
    def test_get(self):
        f = Foo()
        assert_raises(IOError, f.get)
    def test_calc(self):
        f = Foo()
        assert f.calc(self.multiplier) != 5