-- https://neovim.io/doc/user/lua.html#_lua-module:-vim.ui
vim.ui.input({prompt = 'Enter value for shiftwidth: '}, function(input)
    local num = tonumber(input)
    vim.notify(string.format("\n%s\n", num), vim.log.levels.DEBUG)
end)
