local function trace(event, line)
    local info = debug.getinfo(2)
    local s = info.short_src
    -- print(string.format("event %s", event))
    print(s .. ":" .. line)
    local line = io.read()
    if line == "c" then
        print("continer")
    else
        print(string.format("function name %s", info.name))
    end
end

local function test()
    local var = "abc"
    print(var)
end

debug.sethook(trace, "l")
test()
