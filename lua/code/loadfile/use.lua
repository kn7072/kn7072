local f = loadfile("./foo.lua")
print(f)
f()
-- assert(f.foo("ok"), "error")
foo("ok")

local status, err = pcall(function() error("my error") end)
if status then
    print("ok")
else
    print(err)
end
