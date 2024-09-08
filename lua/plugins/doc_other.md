https://github.com/VonHeikemen/lsp-zero.nvim/issues/138
:LuaSnipListAvailable
So snippets can come from two sources: luasnip or nvim_lsp.

The ones coming from your LSP server should have this format:

if .. then~     [LSP]     Snippet

The ones from luasnip look like this:

if~     [luasnip]     Snippet

If you don't see the ones from [luasnip] is likely friendly-snippets doesn't support the filetype. You can check the snippets loaded in luasnip with this command:
#######################################################

:checkhealth which-key
#######################################################
:LuaSnipListAvailable
lua require("luasnip").log.open()

:LspInfo информация о текущем lsp
#######################################################
https://stackoverflow.com/questions/73358168/where-can-i-check-my-neovim-lua-runtimepath

:lua print(vim.inspect(vim.api.nvim_list_runtime_paths()))
:lua print(vim.fn.stdpath("data"))  /home/stepan/.local/share/nvim
#######################################################
https://github.com/L3MON4D3/LuaSnip/blob/master/DOC.md#vscode
lua local sl = require("luasnip.extras.snippet_list"); sl.open()

-- making our own snip_info
local function snip_info(snippet)
	return { name = snippet.name }
end

-- using it
sl.open({snip_info = snip_info})



local sl = require("luasnip.extras.snippet_list")
local function display(printer_result)
    -- right vertical split
    vim.cmd("botright vnew")

    -- get buf and win handle
    local buf = vim.api.nvim_get_current_buf()
    local win = vim.api.nvim_get_current_win()

    -- setting window and buffer options
    vim.api.nvim_win_set_option(win, "foldmethod", "manual")
    vim.api.nvim_buf_set_option(buf, "filetype", "javascript")

    vim.api.nvim_buf_set_option(buf, "buftype", "nofile")
    vim.api.nvim_buf_set_option(buf, "bufhidden", "wipe")
    vim.api.nvim_buf_set_option(buf, "buflisted", false)

    vim.api.nvim_buf_set_name(buf, "Custom Display buf " .. buf)

    -- dump snippets
    local replacement = vim.split(printer_result)
    vim.api.nvim_buf_set_lines(buf, 0, 0, false, replacement)
end

-- using it
sl.open({display = display})
