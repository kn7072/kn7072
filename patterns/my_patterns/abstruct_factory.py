# coding: utf-8
"""Паттерн абстрактная фабрика."""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum


class ProductDesing(Enum):
    """Варианты дезайна продуктов."""

    CLASSIC = "classis"
    MODERN = "modern"
    SURREALISM = "surrealism"


class ProductA:
    """Продукт A."""

    def __init__(self: ProductA, design: ProductDesing) -> None:
        """Инициализирует объект."""
        self.design = design


class ProductB:
    """Продукт B."""

    def __init__(self: ProductB, design: ProductDesing) -> None:
        """Инициализирует объект."""
        self.design = design


class Factory(ABC):
    """Фабрика семейства продуктов."""

    @abstractmethod
    def create_product_a(self: Factory) -> ProductA:
        """Создает продукт A."""
        ...

    @abstractmethod
    def create_product_b(self: Factory) -> ProductB:
        """Создает продукт B."""
        ...


class ClassicFactory(Factory):
    """Производит продукты в классическом стиле."""

    design = ProductDesing.CLASSIC

    def create_product_a(self: ClassicFactory) -> ProductA:
        """Создает продукт A."""
        print("Создали ProductA в ClassicFactory")
        return ProductA(self.design)

    def create_product_b(self: ClassicFactory) -> ProductB:
        """Создает продукт B."""
        print("Создали ProductB в ClassicFactory")
        return ProductB(self.design)


class ModernFactory(Factory):
    """Производит продукты в современном стиле."""

    design = ProductDesing.MODERN

    def create_product_a(self: ModernFactory) -> ProductA:
        """Создает продукт A."""
        print("Создали ProductA в ModernFactory")
        return ProductA(self.design)

    def create_product_b(self: ModernFactory) -> ProductB:
        """Создает продукт B."""
        print("Создали ProductB в ModernFactory")
        return ProductB(self.design)


if __name__ == "__main__":
    classic_factory = ClassicFactory()
    modern_factory = ModernFactory()
    classic_product_a = classic_factory.create_product_a()
    modern_product_b = modern_factory.create_product_b()
