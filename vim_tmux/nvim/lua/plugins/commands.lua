local api = vim.api

api.nvim_create_user_command('Flake8', function(opts)
    local cmd = "flake8"
    -- print("flake8")
    if vim.fn.executable(cmd) then
        -- print("flake8", opts.args)
        cmd = string.format("%s %s", cmd, opts.args)
        -- print(vim.fn.system(cmd))

        local output = vim.split(vim.trim(vim.fn.system(cmd)), "\n")
        -- print(vim.inspect(output))
        return output
    end

    -- vim.call("flake8", "%", input.bang)
    -- vim.call('flake8', '~/temp/experimental/py', input.bang)
end, {desc = 'First flake8', nargs = 1, bang = true}) -- bang = true, 

api.nvim_create_user_command('Upper', function(opts)
    print(string.upper(opts.args))
end, {nargs = 1})

vim.api.nvim_create_user_command('Upper2', function(opts)
    print(opts.args)
end, {
    nargs = 1,
    complete = function(ArgLead, CmdLine, CursorPos)
        -- return completion candidates as a list-like table
        return {'foo', 'bar', 'baz'}
    end
})
