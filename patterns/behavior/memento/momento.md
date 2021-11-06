![Снимок дизайн](./momento_design.png)
![Снимок реализация](./momento_implementation.png)


https://python.astrotech.io/design-patterns/behavioral/memento.html

Implementation


```python

from dataclasses import dataclass, field
from typing import Final


@dataclass
class EditorState:
    __content: Final[str]

    def get_content(self):
        return self.__content


@dataclass
class History:
    __states: list[EditorState] = field(default_factory=list)

    def push(self, state: EditorState) -> None:
        self.__states.append(state)

    def pop(self) -> EditorState:
        return self.__states.pop()


class Editor:
    __content: str

    def set_content(self, content: str) -> None:
        self.__content = content

    def get_content(self) -> str:
        return self.__content

    def create_state(self):
        return EditorState(self.__content)

    def restore_state(self, state: EditorState):
        self.__content = state.get_content()


if __name__ == '__main__':
    editor = Editor()
    history = History()

    editor.set_content('a')
    history.push(editor.create_state())
    print(editor.get_content())
    # a

    editor.set_content('b')
    history.push(editor.create_state())
    print(editor.get_content())
    # b

    editor.set_content('c')
    print(editor.get_content())
    # c

    editor.restore_state(history.pop())
    print(editor.get_content())
    # b


 ##### Assignments
from dataclasses import dataclass, field
from typing import Final


@dataclass
class Transaction:
    def get_amount(self):
        raise NotImplementedError


@dataclass
class History:
    def push(self, transaction: Transaction) -> None:
        raise NotImplementedError

    def pop(self) -> Transaction:
        raise NotImplementedError


@dataclass
class Account:
    def deposit(self, amount: float) -> None:
        raise NotImplementedError

    def get_balance(self) -> float:
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def undo(self, transaction: Transaction):
        raise NotImplementedError

# Solution
@dataclass
class Transaction:
    __amount: Final[float]

    def get_amount(self):
        return self.__amount


@dataclass
class History:
    __transactions: list[Transaction] = field(default_factory=list)

    def push(self, transaction: Transaction) -> None:
        self.__transactions.append(transaction)

    def pop(self) -> Transaction:
        return self.__transactions.pop()


@dataclass
class Account:
    __balance: float = 0

    def deposit(self, amount: float) -> None:
        self.__balance += amount

    def get_balance(self) -> float:
        return self.__balance

    def save(self):
        return Transaction(self.__balance)

    def undo(self, transaction: Transaction):
        self.__balance = transaction.get_amount()

>>> account = Account()
>>> history = History()

>>> account.deposit(100.00)
>>> history.push(account.save())
>>> account.get_balance()
100.0

>>> account.deposit(50.00)
>>> history.push(account.save())
>>> account.get_balance()
150.0

>>> account.deposit(25.00)
>>> account.get_balance()
175.0

>>> account.undo(history.pop())
>>> account.get_balance()
150.0

```