local opt = vim.opt
local o = vim.o
local wo = vim.wo

vim.g.did_load_filetypes = 1
vim.g.formatoptions = "qrn1"
opt.showmode = true
opt.updatetime = 100
wo.signcolumn = "yes"
opt.scrolloff = 8
wo.linebreak = true
opt.virtualedit = "block"
opt.undofile = true
opt.shell = "/bin/fish"

-- Mouse
opt.mouse = "a"
opt.mousefocus = true

-- Line Numbers
opt.number = true
opt.relativenumber = true

-- Splits
opt.splitbelow = true
opt.splitright = true

-- Clipboard
opt.clipboard = "unnamedplus"

-- Shorter messages
opt.shortmess:append("c")

-- Indent Settings
opt.expandtab = true
opt.shiftwidth = 4
opt.tabstop = 4
opt.softtabstop = 4
opt.smartindent = true

-- Fillchars
opt.fillchars = {
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
opt.wrap = true

opt.foldnestmax = 100
-- opt.foldmethod = "syntax"
opt.foldcolumn = "1"
o.foldlevel = 99 -- Using ufo provider need a large value, feel free to decrease the value
o.foldlevelstart = 99 -- уровень вложенности фолдов которые будут закрыты, и
-- будут автоматически закрываться, если указать 3, то будут закрыты фолты имеющие двух родительских фолдов
o.foldenable = true

-- чтобы оставалась последняя строка файла(https://neovim.io/doc/user/options.html#'fixeol')
opt.fixeol = true
opt.fixendofline = true

vim.env.PATH = string.format("%s:%s",
                             "/home/stepan/.cache/pypoetry/virtualenvs/kn7072-mq-0OsHe-py3.12/bin",
                             vim.env.PATH)

-- vim.o.guicursor = 'n-v-c-sm-i-ci-ve:block,r-cr-o:hor20,a:blinkwait700-blinkoff400-blinkon250'
-- :h guicursor
vim.o.guicursor = 'i-ci-ve:ver25,a:blinkwait2000-blinkoff2000-blinkon1000'
