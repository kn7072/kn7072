local Object = {a = 1, b = 2}

Object.__index =
    function(_, k) -- не сработает, так как подобные функции должны быть в метатаблице
        return "__init"
    end

local mt = {
    __index = function(_, k)
        return "meta_index"
    end
}
setmetatable(Object, mt) -- __index работает так как находится в метатаблице 

print(Object.xxx) -- meta_index если добавлена мета таблица
