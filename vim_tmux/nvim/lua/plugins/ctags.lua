vim.api.nvim_create_autocmd("BufWritePost", {
    pattern = {"*.go", "*.py"},
    callback = function()
        -- vim.fn.system({'ctags', '-R', '--exclude=.git', '*.go'})
        vim.fn.system({'ctags', '-R', '--exclude=.git', '--exclude=*.sql'})
    end
})
