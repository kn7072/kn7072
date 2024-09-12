local b = 1

local function test()
    local a = ""
    print("a")
end

local function trace(event, line)
    print(string.format("event %s line %s", event, line))
    local info = debug.getinfo(2, "nSLf")
    if event == "call" then
        print(info.name)
        debug.debug()
        local i = io.read()
    end
    if event == "line" then end

end

debug.sethook(trace, "cl")

test()
