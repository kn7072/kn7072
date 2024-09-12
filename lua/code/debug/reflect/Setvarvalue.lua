function Setvarvalue(name, setvalue)
    -- print(debug.traceback("Stack trace"))
    -- for j = 1, math.huge do
    --     local info = debug.getinfo(j)
    --     if info ~= nil then
    --         print(info)
    --     else
    --         print("finish")
    --         break
    --     end
    -- end
    -- print("Stack trace end")

    local exit = false
    for i = 1, math.huge do
        local n, v = debug.getlocal(2, i)
        if not n then break end
        print(string.format("var local %s %s", n, v))

        if n == name then
            debug.setlocal(2, i, setvalue)
            exit = true -- выведим все локальные переменные
            -- return
        end
    end

    if exit then return end

    local func = debug.getinfo(2, "f").func
    for i = 1, math.huge do
        local n, v = debug.getupvalue(func, i)
        if not n then break end
        if n == name then
            debug.setupvalue(func, i, setvalue)
            return
        else
            print(string.format("var %s %s", n, v))
        end
    end
    _ENV[name] = setvalue
end

local f = 10

function Test()
    local b = 30
    local a = 10
    print(a)
    Setvarvalue('a', 20)
    print(a)
    print(f)
    Setvarvalue('f', 30)
    print(f, cc)
    Setvarvalue('cc', 'yyy')
    print(cc)
    local g = 3
    Setvarvalue('g', 20)
    print(g)
end

Test()
