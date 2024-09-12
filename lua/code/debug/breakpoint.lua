--[[
Exercise 25.7

Write a library for breakpoints. It should offer at least two functions:

setbreakpoint(function, line) --> returns handle
removebreakpoint(handle)

We specify a breakpoint by a function and a line inside that function. 
When the program hits a breakpoint, the library should call debug.debug. 
(Hint: for a basic implementation, use a line hook that checks whether it is in a breakpoint; 
to improve performance, use a call hook to trace program execution and only turn on 
the line hook when the program is running the target function.)
--]] local function trace(event, line)
    local info = debug.getinfo(2, "SnlfL")
    -- print(event, line)
    -- name, linedefined, lastlinedefined, func
    -- for i, v in pairs(s) do print(i, v) end
    -- print(string.format("source %s fun name %s", info.source, info.name))
    if event == "call" then
        if info.source == "@breakpoint.lua" and info.name == "test" then
            print("find-------")
            debug.sethook(trace, "l")
        end
    end

    if event == "line" then
        print("line")
        print(event.currentline, line)
        -- if event.currentline == line then
        -- debug.debug()
        -- debug.sethook(trace, "c"RemDebug)
        -- end
    end
end

debug.sethook(trace, "c")

local function setbreakpoint(func, line)
    -- проверить тип func
    local func_info = debug.getinfo(func, "SnLf")
    print(func_info)
    for i, v in pairs(func_info) do print(i, v) end
    print(func_info.name)
    for i, v in pairs(func_info.activelines) do print(i, v) end
    -- func()
end

local function test()
    local var = "test"
    local x = "x"
    local y = {}
    y.z = 8
    print(var)
end

local function test_2() test() end

test()
print("before test_2")
test_2()
print("after_test_2")
setbreakpoint(test, 2)
-- setbreakpoint(print, 1)
