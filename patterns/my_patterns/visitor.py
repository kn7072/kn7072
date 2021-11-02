# coding: utf-8
"""Паттерн посетитель."""
from __future__ import annotations

from abc import ABC, abstractmethod


class Visitor(ABC):
    """Интерфейс посетителя."""

    @abstractmethod
    def visit_component_a(self: Visitor, component: ComponentA) -> str:
        """Метод для работы с visit_component_a."""
        ...

    @abstractmethod
    def visit_component_b(self: Visitor, component: ComponentB) -> str:
        """Метод для работы с visit_component_b."""
        ...


class VisitorA(Visitor):
    """Интерфейс посетителя."""

    def visit_component_a(self: VisitorA, component: ComponentA) -> str:
        """Метод для работы с visit_component_a."""
        component.do_something()
        # еще что-то сделал

    def visit_component_b(self: VisitorA, component: ComponentB) -> str:
        """Метод для работы с visit_component_b."""
        component.do_something_other()
        # еще что-то сделал


class Component(ABC):
    """Интерфейс компонента."""

    @abstractmethod
    def accept(self: Component, visitor: Visitor) -> str:
        """Принимает посетителя."""
        ...

    @abstractmethod
    def do_something(self: Component) -> None:
        """Что-то делает."""
        ...


class ComponentA(Component):
    """Компонент A."""

    def accept(self: ComponentA, visitor: Visitor) -> str:
        """Принимает посетителя."""
        return visitor.visit_component_a(self)

    def do_something(self: ComponentA) -> None:
        """Что-то делает."""
        print("ComponentA")


class ComponentB(Component):
    """Компонент B."""

    def accept(self: ComponentB, visitor: Visitor) -> str:
        """Принимает посетителя."""
        return visitor.visit_component_b(self)

    def do_something(self: ComponentB) -> None:
        """Что-то делает."""
        print("ComponentB")

    def do_something_other(self: ComponentB) -> None:
        """Что-то делает."""
        print("ComponentB")


if __name__ == "__main__":
    component_a = ComponentA()
    component_b = ComponentB()
    visitor_a = VisitorA()

    component_a.accept(visitor_a)
    component_b.accept(visitor_a)
