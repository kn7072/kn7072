local kmap = vim.keymap.set
local nvim_map = vim.api.nvim_set_keymap
local opts = { noremap = true, silent = true }

vim.g.mapleader = " "

-- NeoTree
kmap("n", "<leader>e", ":Neotree float reveal<CR>")
kmap("n", "<leader>o", ":Neotree float git_status<CR>")

-- Navigation
kmap("n", "<c-k>", ":wincmd k<CR>")
kmap("n", "<c-j>", ":wincmd j<CR>")
kmap("n", "<c-h>", ":wincmd h<CR>")
kmap("n", "<c-l>", ":wincmd l<CR>")
kmap("n", "<leader>/", ":CommentToggle<CR>")

-- Other
kmap("n", "<leader>w", ":w<CR>")
kmap("n", "<leader>x", ":BufferLinePickClose<CR>")
kmap("i", "jj", "<Esc>")
kmap("n", "<leader>h", ":nohlsearch<CR>")

-- Tabs
kmap("n", "<Tab>", ":BufferLineCycleNext<CR>")
kmap("n", "<s-Tab>", ":BufferLineCyclePrev<CR>")

-- Terminal
kmap("n", "<leader>tf", ":ToggleTerm direction=float<CR>")
kmap("n", "<leader>th", ":ToggleTerm direction=horizontal<CR>")
kmap("n", "<leader>tv", ":ToggleTerm direction=vertical size=40<CR>")

kmap("n", "gdt", "<cmd>tab split | lua vim.lsp.buf.definition()<CR>", opts)

-- Toggle relative line number
kmap("n", "<c-l><c-l>", ":set invrelativenumber<CR>")

-- ctrl + c
kmap("v", "<leader>cc", '"+y<CR>')

--[[
spell
:set nospell  - чтобы отключить подцветку ошибок

для выбора подходящих слов
z= появится сокращенный список
z=z появится полный список

для исправляния в режиме редактирования
<c-x><c-s>
--]]
kmap("n", "]s", function()
	local spell = vim.wo.spell
	vim.wo.spell = true
	vim.opt.spelllang = { "en_us", "ru_ru" }
	vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes("]s", true, true, true), "n", true)
	-- vim.schedule(function()
	--     vim.wo.spell = spell
	-- end)
end)
