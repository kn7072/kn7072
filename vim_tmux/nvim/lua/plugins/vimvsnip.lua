-- :LuaSnipListAvailable
local luasnip = require("luasnip")
require("luasnip.loaders.from_vscode").lazy_load({
    paths = vim.fn.stdpath("data") .. "/lazy/friendly-snippets"
})
require("luasnip.loaders.from_vscode").load_standalone({
    path = vim.fn.stdpath('config') .. "/my_snippets/a.code-snippets"
})

local path_to_dir_snippets = "~/.config/nvim/my_snippets"
-- require("luasnip.loaders.from_vscode").lazy_load({
--     paths = {path_to_dir_snippets}
-- })
-- для файлов с раширением .json
require("luasnip.loaders.from_vscode").load({paths = {path_to_dir_snippets}})

-- для python.snippets и go.snippets и подобным файлам с расширением .snippets
-- require("luasnip.loaders.from_snipmate").lazy_load({
--     paths = {path_to_dir_snippets}
-- })

-- vim.api.nvim_set_keymap("i", "<C-n>", "<Plug>luasnip-next-choice", {})
-- vim.api.nvim_set_keymap("s", "<C-n>", "<Plug>luasnip-next-choice", {})
-- vim.api.nvim_set_keymap("i", "<C-p>", "<Plug>luasnip-prev-choice", {})
-- vim.api.nvim_set_keymap("s", "<C-p>", "<Plug>luasnip-prev-choice", {})
-- luasnip.parser
--     .parse_snippet({trig = "lsp"}, "$1 is ${2|hard,easy,challenging|}")
vim.keymap.set({"i"}, "<C-k>", function()
    luasnip.expand()
end, {silent = true})
vim.keymap.set({"i", "s"}, "<C-n>", function()
    luasnip.jump(1)
end, {silent = true})
vim.keymap.set({"i", "s"}, "<C-p>", function()
    luasnip.jump(-1)
end, {silent = true})
vim.keymap.set({"i", "s"}, "<C-s>", function()
    -- посмотреть все доступные снипеты
    local sl = require("luasnip.extras.snippet_list")
    sl.open()
end, {silent = true})
vim.keymap.set({"i", "s"}, "<C-e>", function()
    if luasnip.choice_active() then
        luasnip.change_choice(1)
    end
end, {silent = true})

-- would search and expand C and C++ snippets for C++ files.
luasnip.filetype_extend("cpp", {"c", "cpp"})
