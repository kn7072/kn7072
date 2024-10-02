# from  test_package import a
#
# a.a()

# from test_package.a import *
# print()

# import test_package.b as b
#
# print(dir(b))
# print(dir(b.b))

import test_package

print(dir(test_package))
print(type(test_package.a))
print(dir(test_package.a))
print(type(test_package.a.a1))
print("#"*20)
print(type(test_package.b))
print(dir(test_package.b))
print(dir(test_package.b.b1))
print(type(test_package.b.b2))
print()
