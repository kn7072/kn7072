local function trace()
    for i = 1, math.huge do
        local func = debug.getinfo(i, "fn")
        if not func then break end
        print(string.format("func name %s", func.name))
        local f = func.func
        if not f then break end
        for j = 1, math.huge do
            local n, v = debug.getlocal(f, j) -- getupvalue(f, j)
            if not n then
                break
            else
                print(string.format("var %s %s", n, v))
            end
        end
    end
end

local function trace_2()
    for i = 1, math.huge do
        local func = debug.getinfo(i, "fn")
        if not func then break end
        print(string.format("func name %s", func.name))
        local f = func.func
        if not f then break end
        for j = 1, math.huge do
            local n, v = debug.getupvalue(f, j) -- getupvalue(f, j)
            if not n then
                break
            else
                print(string.format("var %s %s", n, v))
            end
        end
    end
end

local function trace_3()
    for i = 1, math.huge do
        local info = debug.getinfo(i)
        if not info then break end
        print(string.format("=== i %d function name %s", i, info.name))
        for j = 1, math.huge do
            local n, v = debug.getlocal(i, j) -- getupvalue(f, j)
            if not n then
                break
            else
                print(string.format("var %s %s", n, v))
            end
        end
    end
end
local global_var = "global"
global_var_2 = "global 2"
local function test_1(x1, x2)
    local a = 1
    local b = 2
    print(x1, x2)
    trace()
    print("#########################")
    trace_2()
    print("#########################")
    trace_3()
end

local function test_2(x1, x2)
    local a = 3
    local b = 4
    test_1(x1 + 1, x2 + 1)
end

local function test_3(x1, x2)
    local a = 5
    local b = 6
    test_2(x1 + 1, x2 + 1)
end

test_3(1, 2)
