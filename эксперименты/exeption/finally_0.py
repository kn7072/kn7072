# coding: utf-8
"""Тестируем поведение return в блоке finally."""


def func1() -> int:
    try:
        return 1  # ignoring the return
    finally:
        return 2  # returns this return


def func2() -> int:
    try:
        raise ValueError()
    except:
        # is going to this exception block, but ignores the return because it needs to go to the finally
        return 1
    finally:
        return 3


def func3() -> int:
    return 0  # finds a return here, before the try except and finally block, so it will use this return 
    try:
        raise ValueError()
    except:
        return 1
    finally:
        return 3


def func4() -> int:
    try:
        raise ValueError()
    except:
        return 1
    finally:
        print("func4 finally")


res1 = func1()  # returns 2
print(res1)
res2 = func2()  # returns 3
print(res2)
res3 = func3()  # returns 0
print(res3)
res4 = func4()  # returns 1
print(res4)
