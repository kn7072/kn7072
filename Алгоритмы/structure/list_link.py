#coding:utf-8

class LinksList:

    _first_element = None
    _last_element = None

    def add_right(self, item, elem=None):

        if elem:
            elem_right = elem[2]
            temp_element = [item, elem, elem_right]
            if elem_right:
                # если не крайний правый
                elem_right[1] = temp_element
            else:
                self._last_element = temp_element   
            elem[2] = temp_element
        else:
            if self._last_element:
                temp_element = [item, self._last_element, None]
                self._last_element[2] = temp_element
            else:
                temp_element = [item, None, None]
                self._first_element = temp_element
            self._last_element = temp_element

    def add_left(self, item, elem=None):
        
        if elem:
            elem_left = elem[1]
            temp_element = [item, elem_left, elem]
            if elem_left:
                elem_left[2] = temp_element
            else:
                self._first_element = temp_element
            elem[1] = temp_element 
            
        else:
            if self._first_element:
                temp_element = [item, None, self._first_element]
                self._first_element[1] = temp_element
            else:
                temp_element = [item, None, None]
                self._last_element = temp_element
            self._first_element = temp_element

    def print_dque(self):
        start_elem = self._first_element
        while True:
            if start_elem:
                print(start_elem[0])
                start_elem = start_elem[2]
            else:
                break    


    
    def remove(self, elem=None):
        # удаляет последний элемент из списка. Не нуждается в параметрах и возвращает элемент. Список модифицируется.
        if elem:
            val = elem[0]
            right = elem[2]
            left = elem[1]
            left[2] = right
            right[1] = left
        
        pass

    
    def size(self):
        # возвращает количество элементов в списке. Не нуждается в параметрах и возвращает целое число.
        pass

    def is_empty(self):
        # проверяет список на пустоту. Не нуждается в параметрах и возвращает булево значение.
        pass


ll = LinksList()

ll.add_left(0)

ll.add_right(1)
ll.add_right(3)
ll.add_left(5)
ll.print_dque()

temp = ll._first_element[2][2]
ll.add_right(7, temp)
ll.add_left(8, temp)
print("#"*15)
ll.print_dque()
print()