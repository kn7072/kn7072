import test_package.a.a1 as x

print(x.a()) # если использовать псевдоним x в импотре import test_package.a.a1 as x

print(dir(test_package.a)) # можно так обратиться, так как вся цепочка импортируется
# если не использовать псевдоним import test_package.a.a1 as x, если испльзовался псевдоним
# тогда нельзя обращаться  test_package.a
