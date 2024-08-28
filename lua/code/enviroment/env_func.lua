local function print_env(env)
    for k, v in pairs(env) do
        print(k, v)
    end
end

local function factory(_ENV)
    print_env(_ENV)

    return function()
        print_env(_ENV)
        -- for k, v in pairs(_ENV) do
        --     print(k, v)
        -- end
        --
        return a
    end
end
f1 = factory {a = 1}
f2 = factory {a = 2}

print("*******")
print_env(_ENV)
print("*******")

print(f1())
print(f2())
