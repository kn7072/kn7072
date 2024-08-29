-- https://fingercomp.gitlab.io/lua-coroutines/
-- Возвращает корутину, в которой вызвана эта функция.
--
-- Вторым значением также возвращает true, если функция вызвана в главном потоке, или false в противном случае.
-- Листинг 3.8. Вызов coroutine.running в корутине
coroutine.resume(coroutine.create(function() print(coroutine.running()) end))

-- Листинг 3.9. Вызов coroutine.running в главном потоке.
print(coroutine.running())
