# coding: utf-8
"""Паттерт строитель."""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum


class ProductType(Enum):
    """Типы продуктов."""

    SIMPLE = "simple"
    MEDIUM = "medium"
    FULL = "full"


class Product:
    """Заготовка для изготовления продукта."""

    def __init__(self: Product) -> None:
        """Инициализирует объект."""
        self.building_stages = []


class Builder(ABC):
    """Интерфейс строителя."""

    @abstractmethod
    def build_step_a(self: Builder) -> None:
        """Что-то делает для построения объекта."""
        ...

    @abstractmethod
    def build_step_b(self: Builder) -> None:
        """Что-то делает для построения объекта."""
        ...

    @abstractmethod
    def build_step_c(self: Builder) -> None:
        """Что-то делает для построения объекта."""
        ...


class ConcreteBuilder(Builder):
    """Реализация строителя."""

    def __init__(self: ConcreteBuilder) -> None:
        """Инициализирует объект."""
        self._product = Product()

    @property
    def product(self: ConcreteBuilder) -> Product:
        """Своисво для получения продукта."""
        return self._product

    def build_step_a(self: ConcreteBuilder) -> None:
        """Что-то делает для построения объекта."""
        msg = "Выполнили шаг - build_step_a из класса (ConcreteBuilder)"
        self._product.building_stages.append(msg)

    def build_step_b(self: ConcreteBuilder) -> None:
        """Что-то делает для построения объекта."""
        msg = "Выполнили шаг - build_step_b из класса (ConcreteBuilder)"
        self._product.building_stages.append(msg)

    def build_step_c(self: ConcreteBuilder) -> None:
        """Что-то делает для построения объекта."""
        msg = "Выполнили шаг - build_step_c из класса (ConcreteBuilder)"
        self._product.building_stages.append(msg)


class Director:
    """Занимается созданием объектов(инкапсулирует алгоритмы создания продуктов)."""

    def __init__(self: Director, builder: Builder) -> None:
        """Инициализирует объект."""
        self._builder = builder

    def change_buider(self: Director, builder: Builder) -> None:
        """Заменяет строителя."""
        self._builder = builder

    def make_product(self: Director, product_type: ProductType) -> Product:
        """Создает продукт."""
        if product_type == ProductType.SIMPLE:
            self._builder.build_step_a()
        elif product_type == ProductType.MEDIUM:
            self._builder.build_step_a()
            self._builder.build_step_b()
        elif product_type == ProductType.FULL:
            self._builder.build_step_a()
            self._builder.build_step_b()
            self._builder.build_step_c()
        else:
            raise Exception(f"Передан неизвестный тип продукта {product_type}")
        return self._builder.product


if __name__ == "__main__":
    builder = ConcreteBuilder()
    director = Director(builder)
    medium_product = director.make_product(ProductType.MEDIUM)
    print(medium_product.building_stages)

    full_product = director.make_product(ProductType.FULL)
    print(full_product.building_stages)
