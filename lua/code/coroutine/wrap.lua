-- coroutine.wrap(f)
--
--     Создаёт новую корутину из функции f.
--
--     Возвращает новую функцию: при её вызове корутина возобновляется с переданными аргументами. Возвращает эта функция всё, что передаст корутина.
--
--     Если возникает ошибка, coroutine.wrap не перехватывает её, в отличие от coroutine.resume.
--     Листинг 3.10. Вариант coroutine.wrap на чистом Lua.
function coroutine.wrap(f)
    local co = coroutine.create(f)

    return function(...)
        local executionResult = table.pack(coroutine.resume(co, ...))

        if executionResult[1] then
            return table.unpack(executionResult, 2, executionResult.n) -- 1
        else
            error(executionResult[2], 2)
        end
    end
end

-- 1 coroutine.wrap возвращает только то, что передала корутина. 
-- Этим она также отличается от coroutine.resume: та добавляет ещё true/false первым значением.
