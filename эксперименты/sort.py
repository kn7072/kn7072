sortList = ['a', 'cc', 'bbb']
sortList2 = [[7,'f'],[3,'a'], [2,'cc'], [5,'bbb']]
# Создаем "внешнюю" функцию, которая будет сортировать список в алфавитном порядке:
def sortByAlphabet(inputStr):
        return inputStr[0] # Ключом является первый символ в каждой строке, сортируем по нему

# Вторая функция, сортирующая список по длине строки:
def sortByLength(inputStr):
        return len(inputStr) # Ключом является длина каждой строки, сортируем по длине

newList = sorted(sortList2, key=sortByAlphabet)

for_sort = ['ффффф', 'аааааа', "zzzz"]
for_sort.sort(key=lambda x: x[0])
print(for_sort)