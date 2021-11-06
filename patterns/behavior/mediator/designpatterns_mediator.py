"""
* Assignment: DesignPatterns Behavioral Mediator
* Complexity: medium
* Lines of code: 15 lines
* Time: 21 min

English:
    1. Implement Mediator pattern
    2. Create form with Username, Password and Submit button
    3. If Username and Password are provided enable Submit button
    4. Run doctests - all must succeed

Polish:
    1. Zaimplementuj wzorzec Mediator
    2. Stwórz formularz logowania z Username, Password i przyciskiem Submit
    3. Jeżeli Username i Password odblokuj przycisk Submit
    4. Uruchom doctesty - wszystkie muszą się powieść

Tests:
    >>> form = LoginForm()
    >>> form.set_username('root')
    >>> form.set_password('')
    >>> form.submit()
    Traceback (most recent call last):
    PermissionError: Cannot submit form without Username and Password

    >>> form = LoginForm()
    >>> form.set_username('root')
    >>> form.set_password('MyVoiceIsMyPasswordVerifyMe')
    >>> form.submit()
    'Submitted'
"""
from __future__ import annotations
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class UIElement(metaclass=ABCMeta):
    _name: str
    _owner: Form
    _value: Any

    def changed(self):
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value: Any) -> None: ...

    @abstractmethod
    def get_value(self) -> Any: ...


@dataclass
class Input(UIElement):
    _value: str = ''

    def get_value(self) -> str:
        raise NotImplementedError

    def set_value(self, value: str) -> None:
        raise NotImplementedError


@dataclass
class Button(UIElement):
    _value: bool = False

    def set_value(self, value: bool) -> None:
        raise NotImplementedError

    def get_value(self) -> Any:
        raise NotImplementedError

    def enable(self):
        self.set_value(True)

    def disable(self):
        self.set_value(False)

    def is_enabled(self) -> bool:
        return self._value


class Form(metaclass=ABCMeta):
    @abstractmethod
    def on_change(self): ...


class LoginForm(Form):
    username_input: Input
    password_input: Input
    submit_button: Button

    def __init__(self):
        raise NotImplementedError

    def set_username(self, username: str):
        raise NotImplementedError

    def set_password(self, password: str):
        raise NotImplementedError

    def on_change(self):
        raise NotImplementedError

    def submit(self):
        if self.submit_button.is_enabled():
            return 'Submitted'
        else:
            raise PermissionError('Cannot submit form without Username and Password')


# Solution
@dataclass
class UIElement(metaclass=ABCMeta):
    _name: str
    _owner: Form
    _value: Any

    def changed(self):
        self._owner.on_change()

    @abstractmethod
    def set_value(self, value: Any) -> None: ...

    @abstractmethod
    def get_value(self) -> Any: ...


@dataclass
class Input(UIElement):
    _value: str = ''

    def get_value(self) -> str:
        return self._value

    def set_value(self, value: str) -> None:
        self._value = value
        self.changed()


@dataclass
class Button(UIElement):
    _value: bool = False

    def set_value(self, value: bool) -> None:
        self._value = value

    def get_value(self) -> Any:
        return self._value

    def enable(self):
        self.set_value(True)

    def disable(self):
        self.set_value(False)

    def is_enabled(self) -> bool:
        return self._value


class Form(metaclass=ABCMeta):
    @abstractmethod
    def on_change(self): ...


class LoginForm(Form):
    username_input: Input
    password_input: Input
    submit_button: Button

    def __init__(self):
        self.username_input = Input('Username', self)
        self.password_input = Input('Password', self)
        self.submit_button = Button('Submit', self)

    def set_username(self, username: str):
        self.username_input.set_value(username)

    def set_password(self, password: str):
        self.password_input.set_value(password)

    def on_change(self):
        username = self.username_input.get_value()
        password = self.password_input.get_value()
        if username and password:
            self.submit_button.enable()

    def submit(self):
        if self.submit_button.is_enabled():
            return 'Submitted'
        else:
            raise PermissionError('Cannot submit form without Username and Password')
