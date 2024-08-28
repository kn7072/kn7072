a = "glob" -- попадет в _ENV
local a = "local"

local function print_env()
    for k, v in pairs(_ENV) do
        print(k, v)
    end
end

local function env_variable_print()
    print(x)
end

print(a)
print_env()

_ENV["x"] = 100
x = 200 -- переписывает значение из строки выше
print_env()
env_variable_print()
