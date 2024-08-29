function setDefault(t, d)
    local mt = {
        __index = function()
            return d
        end
    }
    setmetatable(t, mt)
end
-- 172 Tables with default values
tab = {x = 10, y = 20}
print(tab.x, tab.z)
setDefault(tab, 0)
--[[
After the call to setDefault, any access to an absent field in tab calls its __index metamethod,
which returns zero (the value of d for this metamethod).
The function setDefault creates a new closure plus a new metatable for each table that needs a default
value. This can be expensive if we have many tables that need default values. However, the metatable has
the default value d wired into its metamethod, so we cannot use a single metatable for tables with different
default values. To allow the use of a single metatable for all tables, we can store the default value of each
table in the table itself, using an exclusive field. If we are not worried about name clashes, we can use a
key like "___" for our exclusive field:
--]]
print(tab.x, tab.z)

local mt = {
    __index = function(t)
        return t.___
    end
}
function setDefault(t, d)
    t.___ = d
    setmetatable(t, mt)
end

--[[
Note that now we create the metatable mt and its corresponding metamethod only once, outside SetDe-
fault.
If we are worried about name clashes, it is easy to ensure the uniqueness of the special key. All we need
is a new exclusive table to use as the key:
--]]
local key = {}
-- unique key
local mt = {
    __index = function(t)
        return t[key]
    end
}
function setDefault(t, d)
    t[key] = d
    setmetatable(t, mt)
end
--[[
An alternative approach for associating each table with its default value is a technique I call dual represen-
tation, which uses a separate table where the indices are the tables and the values are their default values.
However, for the correct implementation of this approach, we need a special breed of table called weak
tables, and so we will not use it here; we will return to the subject in Chapter 23, Garbage.
--]]
