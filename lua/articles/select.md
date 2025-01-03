[источник](https://learntutorials.net/ru/lua/topic/4475/%D0%B2%D0%B0%D1%80%D0%B8%D0%B0%D0%B4%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B5-%D0%B0%D1%80%D0%B3%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B)

Вступление

Varargs , как они обычно известны, позволяют выполнять произвольное количество аргументов без спецификации. Все аргументы, заданные такой функции, упаковываются в единую структуру, известную как список vararg ; который написан как ... в Луа. Существуют основные методы для извлечения числа заданных аргументов и значения этих аргументов с помощью функции select() , но более продвинутые шаблоны использования могут использовать структуру для полной утилиты.
Синтаксис

    ... - Делает функцию, список аргументов которой, в которой появляется переменная функция
    select (what, ...) - Если «what» - это число в диапазоне 1 к числу элементов в vararg, возвращает элемент «what'th» последнему элементу в vararg. Возврат будет равен нулю, если индекс не соответствует границам. Если «что» является строкой «#», возвращается количество элементов в vararg. 

замечания

КПД

Список vararg реализуется как связанный список в реализации языка PUC-Rio, это означает, что индексы O (n). Это означает, что итерация по элементам в vararg с помощью select() , как и в примере ниже, является операцией O (n ^ 2).

for i = 1, select('#', ...) do
    print(select(i, ...))
end

Если вы планируете повторять элементы в списке vararg, сначала упакуйте список в таблицу. Доступ к таблице - это O (1), поэтому повторение выполняется полностью O (n). Или, если вы так склонны, см. Пример foldr() из расширенного раздела использования; он использует рекурсию для итерации по списку vararg в O (n).

Определение длины последовательности

Vararg полезен тем, что длина vararg соответствует любым явно переданным (или вычисленным) нулям. Например.

function test(...)
    return select('#', ...)
end

test()             --> 0
test(nil, 1, nil)  --> 3

Однако это поведение противоречит поведению таблиц, когда оператор длины # не работает с «дырками» (внедренными нилями) в последовательности. Вычисление длины таблицы с отверстиями не определено и на него нельзя положиться. Таким образом, в зависимости от значений в ... , длина {...} не может привести к «правильному» ответу. В Lua 5.2+ для управления этим недостатком был введен table.pack() (в примере реализована функция, реализующая эту функцию в чистом Lua).

Идиоматическое использование

Поскольку varargs несут свою длину, люди используют их как последовательности, чтобы избежать проблем с отверстиями в таблицах. Это не было их предполагаемое использование, и одна эталонная реализация Lua не оптимизирована. Хотя такое использование рассматривается в примерах, оно, как правило, неодобрительно.
основы

Функции Variadic создаются с использованием синтаксиса ... эллипсов в списке аргументов определения функции.

function id(...)
    return
end

Если вы назвали эту функцию id(1, 2, 3, 4, 5) тогда ... (AKA - список vararg) будет содержать значения 1, 2, 3, 4, 5 .

Функции могут принимать требуемые аргументы, а также ...

function head(x, ...)
    return x
end

Самый простой способ вытащить элементы из списка vararg - просто назначить переменные из него.

function head3(...)
    local a, b, c = ...
    return a, b, c
end

select() также может использоваться для поиска количества элементов и извлечения элементов из ... косвенно.

function my_print(...)
    for i = 1, select('#', ...) do
        io.write(tostring(select(i, ...)) .. '\t')
    end
    io.write '\n'
end

... могут быть упакованы в таблицу для удобства использования, используя {...} . Это помещает все аргументы в последовательную часть таблицы.
5,2

table.pack(...) также можно использовать для упаковки списка vararg в таблицу. Преимущество table.pack(...) состоит в том, что он устанавливает поле n возвращенной таблицы в значение select('#', ...) . Это важно, если список аргументов может содержать nils (см. Раздел ниже).

function my_tablepack(...)
    local t = {...}
    t.n = select('#', ...)
    return t
end

Список vararg также может быть возвращен из функций. Результат - несколько возвратов.

function all_or_none(...)
    local t = table.pack(...)
    for i = 1, t.n do
        if not t[i] then
            return    -- return none
        end
    end
    return ...    -- return all
end

Расширенное использование

Как указано в основных примерах, вы можете иметь переменные связанные переменные и список аргументов переменных ( ... ). Вы можете использовать этот факт, чтобы рекурсивно разделить список, как на других языках (например, Haskell). Ниже приведена реализация foldr() которая использует это. Каждый рекурсивный вызов связывает головку списка vararg с x и передает остальную часть списка рекурсивному вызову. Это разрушает список, пока не будет только один аргумент ( select('#', ...) == 0 ). После этого каждое значение применяется к аргументу функции f с ранее вычисленным результатом.

function foldr(f, ...)
    if select('#', ...) < 2 then return ... end
    local function helper(x, ...)
        if select('#', ...) == 0 then
          return x
        end
        return f(x, helper(...))
    end
    return helper(...)
end

function sum(a, b)
    return a + b
end

foldr(sum, 1, 2, 3, 4)
--> 10    

Вы можете найти другие определения функций, которые используют этот стиль программирования здесь в выпуске № 3 по номеру 8.

Единственная идиоматическая структура данных Lua - это таблица. Оператор длины таблицы не определен, если nil s находится где угодно в последовательности. В отличие от таблиц, список vararg учитывает явные значения nil s, как указано в базовых примерах и в разделе замечаний (пожалуйста, прочитайте этот раздел, если вы еще этого не сделали). При небольшой работе список vararg может выполнять каждую операцию, кроме таблицы, помимо мутации. Это делает список vararg хорошим кандидатом для реализации неизменяемых кортежей.

function tuple(...)
    -- packages a vararg list into an easily passable value
    local co = coroutine.wrap(function(...)
        coroutine.yield()
        while true do
            coroutine.yield(...)
        end
    end)
    co(...)
    return co
end

local t = tuple((function() return 1, 2, nil, 4, 5 end)())

print(t())                 --> 1    2    nil    4    5    | easily unpack for multiple args
local a, b, d = t()        --> a = 1, b = 2, c = nil      | destructure the tuple
print((select(4, t())))    --> 4                          | index the tuple
print(select('#', t()))    --> 5                          | find the tuple arity (nil respecting)

local function change_index(tpl, i, v)
    -- sets a value at an index in a tuple (non-mutating)
    local function helper(n, x, ...)
        if select('#', ...) == 0 then
            if n == i then
                return v
            else
                return x
            end
        else
            if n == i then
                return v, helper(n+1, ...)
            else
                return x, helper(n+1, ...)
            end
        end
    end
    return tuple(helper(1, tpl()))
end

local n = change_index(t, 3, 3)
print(t())                 --> 1    2    nil    4    5
print(n())                 --> 1    2    3    4    5

Основное различие между тем, что выше и таблицами, состоит в том, что таблицы изменяемы и имеют семантику указателя, где кортеж не имеет этих свойств. Кроме того, кортежи могут содержать явные nil s и иметь операцию с бесконечной длиной. 