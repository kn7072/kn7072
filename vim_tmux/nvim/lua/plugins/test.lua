local plugin = require("example-plugin")
local ok, whid = pcall(require, "whid")
if not ok then print("error") end
-- plugin.x()

vim.opt.runtimepath:append('~/LUA/repo/debugger_my')
