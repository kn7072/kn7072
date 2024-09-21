local table_with_holes = {[1] = "value_1", [3] = "value_3"}
local mixed_table = {[1] = "value_1", ["not_numeric_index"] = "value_2"}

print("ipairs")
for i, v in ipairs(table_with_holes) do
    print(i, v)
end

print("pairs")
for i, v in pairs(table_with_holes) do
    print(i, v)
end
print("#####")

for i, v in ipairs(mixed_table) do
    print(i, v)
end
