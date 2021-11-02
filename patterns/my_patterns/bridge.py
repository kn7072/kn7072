# coding: utf-8
"""Паттерн мост."""
from __future__ import annotations

from abc import ABC, abstractmethod


class RemoteControl(ABC):
    """Интерфейс абстракции."""

    def __init__(self: RemoteControl, tv_implementation: InterfaceTV) -> None:
        """Инициализация объекта."""
        self._tv_implementation = tv_implementation

    @abstractmethod
    def on(self: RemoteControl) -> None:
        """Влючает устройство."""
        ...

    @abstractmethod
    def off(self: RemoteControl) -> None:
        """Выключает устройство."""
        ...

    @abstractmethod
    def set_channel(self: RemoteControl, channel_number: int) -> None:
        """Переключает канал."""
        ...


class InterfaceTV(ABC):
    """Интерфейс телевизор(реализации)."""

    @abstractmethod
    def on(self: InterfaceTV) -> None:
        """Включить телевизор."""
        ...

    @abstractmethod
    def off(self: InterfaceTV) -> None:
        """Выключить телевизор."""
        ...

    @abstractmethod
    def tune_channel(self: RemoteControl, channel_number: int) -> None:
        """Переключить канал."""
        ...


class SonyTV(InterfaceTV):
    """Реализация телевизора Sony."""

    def on(self: SonyTV) -> None:
        """Включить телевизор."""
        print("Включил телевизор Sony.")

    def off(self: SonyTV) -> None:
        """Выключить телевизор."""
        print("Выключил телевизор Sony.")

    def tune_channel(self: SonyTV, channel_number: int) -> None:
        """Переключить канал."""
        print(f"Переключил канал на {channel_number} (телевизор Sony).")


class ConcreteRemoteControl(RemoteControl):
    """Реализация пульта управления телевизором."""

    def on(self: RemoteControl) -> None:
        """Влючает устройство."""
        self._tv_implementation.on()

    def off(self: RemoteControl) -> None:
        """Выключает устройство."""
        self._tv_implementation.off()

    def set_channel(self: RemoteControl, channel_number: int) -> None:
        """Переключает канал."""
        self._tv_implementation.tune_channel(channel_number)


if __name__ == "__main__":
    sony_tv = SonyTV()
    remote_control = ConcreteRemoteControl(sony_tv)

    remote_control.on()
    remote_control.set_channel(1)
    remote_control.set_channel(2)
    remote_control.off()
