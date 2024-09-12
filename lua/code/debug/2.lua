-- https://www.tutorialspoint.com/lua/lua_debugging.htm
function newCounter()
    local n = 0
    local k = 0
    local y = 10

    return function()
        x = 10
        k = n
        n = n + 1
        y = 100
        return n
    end

end

counter = newCounter()

print(counter())
print(counter())

local i = 0

repeat
    name, val = debug.getupvalue(counter, i)
    -- print("index loop ", i)
    print(name, val)
    if name then
        print("index", i, name, "=", val)

        if (name == "n") then debug.setupvalue(counter, 2, 10) end

        -- i = i + 1
    end -- if
    i = i + 1
    -- print("end loop ", i)
until i >= 5
print("end ", i)
local read = io.read()
print("=>" .. read .. "\n")

print(counter())
