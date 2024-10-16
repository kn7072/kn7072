vim.g.mapleader = " "

-- NeoTree
vim.keymap.set('n', '<leader>e', ':Neotree float reveal<CR>')
vim.keymap.set('n', '<leader>o', ':Neotree float git_status<CR>')

-- Navigation
vim.keymap.set('n', '<c-k>', ':wincmd k<CR>')
vim.keymap.set('n', '<c-j>', ':wincmd j<CR>')
vim.keymap.set('n', '<c-h>', ':wincmd h<CR>')
vim.keymap.set('n', '<c-l>', ':wincmd l<CR>')
vim.keymap.set('n', '<leader>/', ':CommentToggle<CR>')

-- Splits
vim.keymap.set('n', '|', ':vsplit<CR>')
vim.keymap.set('n', '\\', ':split<CR>')

-- Other
vim.keymap.set('n', '<leader>w', ':w<CR>')
vim.keymap.set('n', '<leader>x', ':BufferLinePickClose<CR>')
vim.keymap.set('i', 'jj', '<Esc>')
vim.keymap.set('n', '<leader>h', ':nohlsearch<CR>')

-- Tabs
vim.keymap.set('n', '<Tab>', ':BufferLineCycleNext<CR>')
vim.keymap.set('n', '<s-Tab>', ':BufferLineCyclePrev<CR>')

-- Terminal
vim.keymap.set('n', '<leader>tf', ':ToggleTerm direction=float<CR>')
vim.keymap.set('n', '<leader>th', ':ToggleTerm direction=horizontal<CR>')
vim.keymap.set('n', '<leader>tv', ':ToggleTerm direction=vertical size=40<CR>')

vim.keymap.set("n", "gdt", "<cmd>tab split | lua vim.lsp.buf.definition()<CR>",
               opts)

-- Toggle relative line number
vim.keymap.set('n', '<c-l><c-l>', ':set invrelativenumber<CR>')

-- ctrl + c
vim.keymap.set('v', '<leader>cc', '"+y<CR>')

--[[
spell
:set nospell  - чтобы отключить подцветку ошибок

для выбора подходящих слов
z= появится сокращенный список
z=z появится полный список

для исправляния в режиме редактирования
<c-x><c-s>
--]]
vim.keymap.set('n', ']s', function()
    local spell = vim.wo.spell
    vim.wo.spell = true
    vim.opt.spelllang = {"en_us", "ru_ru"}
    vim.api.nvim_feedkeys(
        vim.api.nvim_replace_termcodes(']s', true, true, true), 'n', true)
    -- vim.schedule(function()
    --     vim.wo.spell = spell
    -- end)
end)
