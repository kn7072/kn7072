local function serialize(o)
    local t = type(o)
    if t == "number" or t == "string" or t == "boolean" or t == "nil" then
        io.write(string.format("%q", o))
    elseif t == "table" then
        io.write("{\n")
        for k, v in pairs(o) do
            io.write(" ", k, " = ")
            serialize(v)
            io.write(",\n")
        end
        io.write("}\n")
    else
        error("cannot serialize a" .. type(o))
    end
end

local test = {
    a = 12,
    b = "Lua",
    key = "another 'one'",
    t = {a = 1, b = 2, c = "xxx"}
}
serialize(test)
