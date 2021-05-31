# coding:utf-8

class Heap:

    _array = []

    def add(self, val):
        self._array.append(val)
        self.up(len(self._array) - 1)

    def up(self, ind):
        parrent_id = (ind - 1) // 2
        if parrent_id >= 0:
            if self._array[parrent_id] > self._array[ind]:
                    self._array[parrent_id], self._array[ind] = self._array[ind], self._array[parrent_id]
                    self.up(parrent_id)

    def print(self):
        print(self._array)  

    def down(self, ind):
        temp_ind = ind
        last_ind = len(self._array) - 1
        left_child = 2 * ind + 1
        right_child = 2 * ind + 2
        if left_child < last_ind and self._array[left_child] < self._array[ind]:
            temp_ind = left_child
        if right_child < last_ind and self._array[right_child] < self._array[temp_ind]:
            temp_ind = right_child
        if temp_ind != ind:
            self._array[temp_ind], self._array[ind] = self._array[ind], self._array[temp_ind]
            self.down(temp_ind)

    
    def pop(self):
        a_0 = self._array[0]
        last_ind = len(self._array) - 1
        self._array[0], self._array[last_ind] = self._array[last_ind], self._array[0]
        del self._array[last_ind]
        self.down(0)
        return a_0                    


heap = Heap()
test_array = [2, 3, 4, 1, 0, 5, 7, 8, 9]
for i in test_array:
    heap.add(i)

heap.print()    

for i in range(6):
    print(heap.pop())

