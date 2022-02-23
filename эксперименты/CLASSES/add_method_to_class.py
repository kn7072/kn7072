# coding:utf-8
"""Добавим метод к классу на лету."""


class Test:
    """Экспериментальный класс."""

    def method_1(self) -> None:
        """Просто метод."""
        print("method_1")


def method_2(self, a: str) -> None:
    """Метод который будет добавлен к классу."""
    print(f"method_2 a = {a}")


if __name__ == "__main__":
    test = Test()
    Test.method_2 = method_2
    test.method_2(10)
