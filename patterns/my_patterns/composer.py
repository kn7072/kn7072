# coding: utf-8
"""Паттерт компоновщик."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional


class Component(ABC):
    """Интейрфейс элементов структуры."""

    def __init__(self: Component) -> None:
        """Инициализирует экземпляр класса."""
        self._children_of_node: List[Component] = []

    def add_child(self: Component, component: Component) -> None:
        """Добавляет дочерний элемент к узлу.

        param component: дочерний узел.
        """
        self._children_of_node.append(component)

    def get_children_node(self: Component) -> Optional[List[Component]]:
        """Возвращает дочерние узлы."""
        return self._children_of_node

    @abstractmethod
    def operation(self: Component) -> None:
        """Делает что-то полезное."""
        ...


class Node(Component):
    """Узел."""

    def __init__(self: Component, node_name: str) -> None:
        """Инициализирует экземпляр класса."""
        super().__init__()
        self.node_name = node_name

    def operation(self: Component) -> None:
        """Обход в грубину."""
        print(self.node_name)
        for node_i in self._children_of_node:
            node_i.operation()


if __name__ == "__main__":
    root_node = Node("root")
    left_node = Node("left")
    right_node = Node("right")
    left_left_node = Node("left_left")
    right_left_node = Node("right_left")
    root_node.add_child(left_node)
    root_node.add_child(right_node)
    left_node.add_child(left_left_node)
    left_node.add_child(right_left_node)
    root_node.operation()
