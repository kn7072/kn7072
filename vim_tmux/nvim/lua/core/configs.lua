vim.wo.number = true
vim.wo.relativenumber = true

vim.g.did_load_filetypes = 1
vim.g.formatoptions = "qrn1"
vim.opt.showmode = true
vim.opt.updatetime = 100
vim.wo.signcolumn = "yes"
vim.opt.scrolloff = 8
vim.wo.linebreak = true
vim.opt.virtualedit = "block"
vim.opt.undofile = true
vim.opt.shell = "/bin/fish"

-- Mouse
vim.opt.mouse = "a"
vim.opt.mousefocus = true

-- Line Numbers
vim.opt.number = true
vim.opt.relativenumber = true

-- Splits
vim.opt.splitbelow = true
vim.opt.splitright = true

-- Clipboard
vim.opt.clipboard = "unnamedplus"

-- Shorter messages
vim.opt.shortmess:append("c")

-- Indent Settings
vim.opt.expandtab = true
vim.opt.shiftwidth = 4
vim.opt.tabstop = 4
vim.opt.softtabstop = 4
vim.opt.smartindent = true

-- Fillchars
vim.opt.fillchars = {
    vert = "│",
    fold = "⠀",
    eob = " ", -- suppress ~ at EndOfBuffer
    -- diff = "⣿", -- alternatives = ⣿ ░ ─ ╱
    msgsep = "‾",
    foldopen = "▾",
    foldsep = "│",
    foldclose = "▸"
}

vim.cmd([[highlight clear LineNr]])
vim.cmd([[highlight clear SignColumn]])

-- переносить длинные строки
vim.opt.wrap = true

vim.opt.foldnestmax = 100
-- vim.opt.foldmethod = "syntax"
vim.opt.foldcolumn = "1"
vim.o.foldlevel = 99 -- Using ufo provider need a large value, feel free to decrease the value
vim.o.foldlevelstart = 99 -- уровень вложенности фолдов которые будут закрыты, и 
-- будут автоматически закрываться, если указать 3, то будут закрыты фолты имеющие двух родительских фолдов
vim.o.foldenable = true

-- чтобы оставалась последняя строка файла(https://neovim.io/doc/user/options.html#'fixeol')
vim.opt.fixeol = true
vim.opt.fixendofline = true

vim.env.PATH = string.format("%s:%s",
                             "/home/stepan/.cache/pypoetry/virtualenvs/telegrambot-0pEd2Avk-py3.12/bin",
                             vim.env.PATH)
