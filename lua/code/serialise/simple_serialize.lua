local fmt = {integer = "%d", float = "%a"}

local function old_serialize(o)
    if type(o) == "number" then
        io.write(string.format(fmt[math.type(o)], o))
    elseif type(o) == "string" then
        io.write(string.format("%q", o))
    end
end

local function serialize(o)
    local t = type(o)
    if t == "number" or t == "string" or t == "boolean" or t == "nil" then
        io.write(string.format("%q\n", o))
    end
end

serialize(5)
serialize(3.5)
serialize(true)
serialize(nil)
