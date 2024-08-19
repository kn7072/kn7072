local T = {[1] = 2, [2] = 5, [10] = 10}

local lengthNum = 0

for k, v in pairs(T) do -- for every key in the table with a corresponding non-nil value 
    lengthNum = lengthNum + 1
end

print(lengthNum)
print(#T)
