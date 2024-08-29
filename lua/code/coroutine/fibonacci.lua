local function fibonacciSeq(n)
    return coroutine.wrap(function()
        local penutimate, previos = 1, 0
        for _ = 1, n do
            penutimate, previos = previos, penutimate + previos
            coroutine.yield(previos)
        end
    end)
end

for n in fibonacciSeq(10) do print(n) end
