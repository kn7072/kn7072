local api = vim.api

api.nvim_create_user_command('Flake8', function(opts)
    local cmd = "flake8"
    -- print("flake8")
    if vim.fn.executable(cmd) then
        -- print("flake8", opts.args)
        cmd = string.format("%s %s", cmd, opts.args)
        -- print(vim.fn.system(cmd))

        local output = vim.split(vim.trim(vim.fn.system(cmd)), "\n")
        print(vim.inspect(output))
        return output
    end

end, {desc = 'First flake8', nargs = 1, bang = true})

api.nvim_create_user_command('Upper', function(opts)
    print(string.upper(opts.args))
end, {nargs = 1})

api.nvim_create_user_command('Tags', function(opts)
    local cursor_word = vim.fn.expand("<cword>")
    print(cursor_word)
    print(vim.inspect(vim.fn.taglist(string.format("^%s", cursor_word))))
end, {desc = "Find tags"})

vim.api.nvim_create_user_command('Upper2', function(opts)
    print(opts.args)
end, {
    nargs = 1,
    complete = function(ArgLead, CmdLine, CursorPos)
        -- return completion candidates as a list-like table
        return {'foo', 'bar', 'baz'}
    end
})

api.nvim_create_user_command('Test', function(opts)
    -- print(string.upper(opts.args))
    print("xxxx")
    api.nvim_set_hl(0, "FoldColumn",
                    {ctermbg = 70, bg = "#d72323", fg = "#11cbd7", bold = true})
end, {})
