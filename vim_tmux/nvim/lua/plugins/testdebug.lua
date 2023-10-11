local function trace(event, line)
    local s = debug.getinfo(2).short_src
    print(s .. ":" .. s)
    local i = io.read()
    print(i)
end
print("xxxxxxx")
-- debug.sethook(trace, "c", 10)
-- debug.debug()
