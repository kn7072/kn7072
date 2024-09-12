function foo(a, b)
    local x
    do local c = a - b end
    local a = 1
    while true do
        local name, value = debug.getlocal(1, a) -- a
        if not name then break end
        print(name, value)
        a = a + 1
    end
end

function foo2()
    local x
    local a = 1
    while true do
        local name, value = debug.getlocal(1, a) -- a
        if not name then break end
        print(name, value)
        a = a + 1
    end
end

dbg()
foo(10, 20)
foo2()
