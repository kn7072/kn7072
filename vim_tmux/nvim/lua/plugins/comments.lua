local api = vim.api

require('nvim_comment').setup({
    line_mapping = "<leader>cl",
    operator_mapping = "<leader>c",
    hook = function()
        local filetype = api.nvim_buf_get_option(0, "filetype")
        if filetype == "c" or filetype == "cpp" then
            api.nvim_buf_set_option(0, "commentstring", "// %s")
        end
    end
})
