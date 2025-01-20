vim.api.nvim_create_autocmd("BufWritePost", {
    pattern = {"*.go", "*.py", "*.c", "*.h"},
    callback = function()
        -- vim.fn.system({'ctags', '-R', '--exclude=.git', '*.go'})
        vim.fn.system( -- {
        --     'ctags', '-R', '−f *.c', '−f *.go', '−f *.py',
        --     '--exclude=.git', '--exclude=*.sql'
        -- }
        {'ctags', '-R', '--languages=C,C++,Python,Go,Lua,Sh'})
    end
})
