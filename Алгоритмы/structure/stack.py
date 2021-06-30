#coding:utf-8

class Stack:
    
    _list = []

    def pop(self):
        # удаляет верхний элемент из стека.
        return self._list.pop() if len(self._list) else None
    
    def push(self, val):
        # добавляет новый элемент на вершину стека.
        self._list.append(val)

    def size(self):
        # возвращает количество элементов в стеке. Параметры не требуются, тип результата - целое число.
        return len(self._list)

    def peek(self):
        # возвращает верхний элемент стека, но не удаляет его. Параметры не требуются, стек не модифицируется.
        return self._list[-1]   
    
    def is_empty(self):
        return bool(self.size)     



stack = Stack()
stack.pop()
print(stack.is_empty())
stack.push(7)
stack.push(3)
stack.push(2)

for _ in range(4):
    print(stack.pop())

