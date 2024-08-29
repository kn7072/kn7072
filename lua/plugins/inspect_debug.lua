for _, win_i in pairs(vim.api.nvim_tabpage_list_wins(0)) do
    local buf_id = tonumber(vim.inspect(vim.api.nvim_win_get_buf(win_i)))
    print(buf_id)
    print(vim.inspect(vim.api.nvim_buf_get_lines(buf_id, 0, 1, false)))
    -- print(type(buf_id))
    local key_map = vim.api.nvim_buf_get_keymap(buf_id, "n")
    if key_map then
        print(vim.inspect(key_map))
    end
    print("*******")
end
