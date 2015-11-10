# -*- coding:utf-8 -*-
class TestContext(object):

    def __init__(self, ignore_error=False):
        self.ignore_error = ignore_error

    def __enter__(self):
        print("__enter__()")
        return self

    def execute(self, error=False):
        print ("execute()")
        if error:
            raise Exception("error")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print ("__exit__(%r, %r, %r)" % (exc_type, exc_val, exc_tb))
        return self.ignore_error


with TestContext() as context:
    context.execute()

with TestContext(ignore_error=True) as context:
    context.execute(error=True)

with TestContext() as context:
    context.execute(error=True)