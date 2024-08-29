local co = coroutine.create(function(a, b, c)
    coroutine.yield(a + b, a - b)
    print("co", a, b, c + 2)
end)

print(coroutine.resume(co, 1, 2, 3))

print(coroutine.status(co))
print(coroutine.resume(co, 0, 0, 0))
print(coroutine.status(co))

function f2()
    print("f2")
    coroutine.yield("yield f2")
    return "end f2"
end

function f1()
    print("f1")
    print("f2 = ", f2())
    print("end f1")
    return "end f1"
end
local co2 = coroutine.create(function() print("f1 = ", f1()) end)

print("###########")
print(coroutine.resume(co2))
print(coroutine.resume(co2))
