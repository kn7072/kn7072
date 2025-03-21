function newCounter()
    local n = 0
    local k = 0
    local x = 3

    return function()
        k = n
        n = n + 1
        x = 1
        return n
    end

end

counter = newCounter()

print(counter())
print(counter())

local i = 1

repeat
    name, val = debug.getupvalue(counter, i)

    if name then
        print("index", i, name, "=", val)

        if (name == "n") then debug.setupvalue(counter, i, 10) end

        i = i + 1
    end -- if

until not name

print(counter())
