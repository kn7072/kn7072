-- https://neovim.io/doc/user/lua.html#_lua-module:-vim.ui
--[[
-- Asynchronous.
vim.ui.open("https://neovim.io/")
vim.ui.open("~/path/to/file")
-- Synchronous (wait until the process exits).
local cmd, err = vim.ui.open("$VIMRUNTIME")
if cmd then
  cmd:wait()
end
--]] --
local cmd, err = vim.ui.open("./ui_input.lua")
if cmd then
    vim.notify(string.format("%s, \nerr = %s", vim.inspect(cmd), err),
               vim.log.levels.DEBUG)
end
