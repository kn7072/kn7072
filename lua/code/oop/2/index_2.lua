-- http://lua-users.org/wiki/ObjectProperties

-- Make proxy object with property support.
-- Notes:
--   If key is found in <getters> (or <setters>), then
--     corresponding function is used, else lookup turns to the
--     <class> metatable (or first to <priv> if <is_expose_private> is true).
--   Given a proxy object <self>, <priv> can be obtained with
--     getmetatable(self).priv .
-- @param class - metatable acting as the object class.
-- @param priv - table containing private data for object.
-- @param getters - table of getter functions
--                  with keys as property names. (default is nil)
-- @param setters - table of setter functions,
--                  with keys as property names. (default is nil)
-- @param is_expose_private - Boolean whether to expose <priv> through proxy.
--                  (default is nil/false)
-- @version 3 - 20060921 (D.Manura)
local function make_proxy(class, priv, getters, setters, is_expose_private)
    setmetatable(priv, class)  -- fallback priv lookups to class
    local fallback = is_expose_private and priv or class
    local index = getters and
      function(self, key)
        -- read from getter, else from fallback
        local func = getters[key]
        if func then return func(self) else return fallback[key] end
      end
      or fallback  -- default to fast property reads through table
    local newindex = setters and
      function(self, key, value)
        -- write to setter, else to proxy
        local func = setters[key]
        if func then func(self, value)
        else rawset(self, key, value) end
      end
      or fallback  -- default to fast property writes through table
    local proxy_mt = {         -- create metatable for proxy object
      __newindex = newindex,
      __index = index,
      priv = priv
    }
    local self = setmetatable({}, proxy_mt)  -- create proxy object
    return self
  end

local Apple = {}
Apple.__index = Apple

function Apple:drop()
    return self.color .. " apple dropped"
  end

local Apple_attribute_setters = {
    color = function(self, color)
        local priv = getmetatable(self).priv
        assert(color == "red" or color == "green")
        priv.color = string.upper(color)
    end
}

function Apple:new()
    local priv = {color = "RED"} -- private attributes in instance
    local self = make_proxy(Apple, priv, nil, Apple_attribute_setters, true)
    return self
end


local a = Apple:new()
assert("RED" == a.color)
a:drop()         -- "RED apple dropped"

a.color = "green"
assert("GREEN apple dropped" == a:drop())
a.color = "red"
assert("RED apple dropped" == a:drop())

a.weight = 123   -- new field
assert(123 == a.weight)

-- fails as expected (invalid color)
local is_ok = pcall(function() a.color = "blue" end)
assert(not is_ok)

