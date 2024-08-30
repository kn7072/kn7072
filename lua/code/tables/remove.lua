-- lua
-- https://uopilot.uokit.com/wiki/index.php?title=Table.remove_(Lua)
local arr = {}
print("clear")
print("mode compact")

table.insert(arr, {1, 2, 3})
table.insert(arr, {4, 5, 6})
table.insert(arr, {7, 8, 9})
-- вывод массива в лог
for i = 1, #arr do
    print(table.concat(arr[i], "   "))
end
print()

local del_elem = table.remove(arr, 2) -- удалить 2-й элемент массива 'arr', при этом оставшиеся будут сдвинуты и размер массива изменится
print("del element " .. table.concat(del_elem))

-- вывод массива в лог
for i = 1, #arr do
    print(table.concat(arr[i], "   "))
end
