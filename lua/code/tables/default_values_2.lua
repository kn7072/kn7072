--[[
Revisiting Tables with Default Values
In the section called “Tables with default values”, we discussed how to implement tables with non-nil
default values. We saw one particular technique and commented that two other techniques needed weak
tables, so we postponed them. Now it is time to revisit the subject. As we will see, these two techniques for
default values are actually particular applications of the two general techniques that we have just discussed:
dual representation and memorization.
In the first solution, we use a weak table to map each table to its default value:
--]] local defaults = {}
setmetatable(defaults, {__mode = "k"})
local mt = {
    __index = function(t)
        return defaults[t]
    end
}

function setDefault(t, d)
    defaults[t] = d
    setmetatable(t, mt)
end
--[[
This is a typical use of a dual representation, where we use defaults[t] to represent t.default. If
the table defaults did not have weak keys, it would anchor all tables with default values into permanent
existence.
In the second solution, we use distinct metatables for distinct default values, but we reuse the same metat-
able whenever we repeat a default value. This is a typical use of memorization:
--]]

local metas = {}
setmetatable(metas, {__mode = "v"})
function setDefault(t, d)
    local mt = metas[d]
    if mt == nil then
        mt = {
            __index = function()
                return d
            end
        }
        metas[d] = mt
        -- memorize
    end
    setmetatable(t, mt)
end

--[[
In this case, we use weak values to allow the collection of metatables that are not being used anymore.
Given these two implementations for default values, which is best? As usual, it depends. Both have similar
complexity and similar performance. The first implementation needs a few memory words for each table
with a default value (an entry in defaults). The second implementation needs a few dozen memory
words for each distinct default value (a new table, a new closure, plus an entry in the table metas). So, if
your application has thousands of tables with a few distinct default values, the second implementation is
clearly superior. On the other hand, if few tables share common defaults, then you should favor the first
implementation.
--]]
