local function get_value(count)
    local tmp = 0
    return function()
        if tmp < count then
            tmp = tmp + 1
            return tmp
        end
    end
end

for j in get_value(5) do print(j) end
