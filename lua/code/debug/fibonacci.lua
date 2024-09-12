function fibonacci(n)
    print(n)
    dbg(n == 2)

    assert(n > 0, "n must be positive")

    -- dbg.assert(0 == 0)

    if n == 1 then
        return 1
    else
        return fibonacci(n - 1) + fibonacci(n - 2)
    end
end

print(package.path)
-- https://stackoverflow.com/questions/18151286/how-to-organize-lua-module-path-and-write-require-calls-without-losing-flexibi
-- package.path = package.path ..
--                    ";/home/stepan/.local/share/nvim/lazy/debugger.lua/?.lua"
print(package.path)
-- vim.opt.runtimepath:append('~/LUA/repo/debugger_my')
-- local path = '/home/stepan/.local/share/nvim/lazy/debugger.lua'
-- print(package.searchpath("debugger", path))

-- res = fibonacci(3)
-- print(res)
dbg = require 'debugger_my'
print(dbg)

dbg()

dbg.call(fibonacci, 3)
print("finish")
