local co = coroutine.create(function(a, b)
    print(a, b)
    local c, d = coroutine.yield(a + b)
    print(c, d)
end)

local success, sum = coroutine.resume(co, 42, 24)
coroutine.resume(co, sum, 12)
coroutine.resume(co, 0, 0)
