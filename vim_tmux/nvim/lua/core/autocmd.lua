vim.api.nvim_create_autocmd("BufReadPost", {
    pattern = "*.pdf",
    callback = function()
        local pdf_reader_name = "okular"
        local file_path = vim.api.nvim_buf_get_name(0)
        -- print(string.format("%s", file_path))
        vim.fn.system({pdf_reader_name, file_path})
    end
})
