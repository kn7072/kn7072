vim.api.nvim_create_autocmd("BufWritePost", {
    callback = function()
        -- vim.fn.system({'ctags', '-R', '--exclude=.git', '*.go'})
        vim.fn.system({'ctags', '-R', '--exclude=.git'})
    end
})
