function traceback()
    for level = 1, math.huge do
        local info = debug.getinfo(level, "Sl")
        if not info then break end
        if info.what == "C" then
            -- is a C function?
            print(string.format("%d\tC function", level))
        else
            -- a Lua function
            print(string.format("%d\t[%s]:%d", level, info.short_src,
                                info.currentline))
        end
    end
end

local function test()
    local a, b = 1, 2
    traceback()
end

local function test_2() test() end

local function test_3()
    print("test_3")
    local info = debug.getinfo(2, "L")
    for _, v in pairs(info.activelines) do print(v) end
end

test_2()
test_3()

for _, v in pairs(debug.getinfo(test_3, "L").activelines) do print(v) end

local func = debug.getinfo(1, "f").func
print(type(func))
for i = 1, math.huge do
    local n, v = debug.getupvalue(func, i)
    if not n then
        break
    else
        print(string.format("%s %s", n, v))
    end
end
