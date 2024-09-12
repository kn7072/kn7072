package.path = package.path .. ";" .. "/home/stepan/LUA/repo/remdebug/src/?.lua"
print(package.path)
print("\n\n")

local socket = require "socket"
local t = "test"

local mod = require "remdebug.engine"
mod.start()

function test()
    local a = 10
    -- debug.debug()
    print(a)
end

test()

print("x")
print("y")
