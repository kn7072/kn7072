vim.opt.termguicolors = true

function SetColor(color)
    color = color or "kanagawa" -- kanagawa onedark
    vim.cmd.colorscheme(color)

    vim.api.nvim_set_hl(0, "Normal", {bg = "#120E27"})
    vim.api.nvim_set_hl(0, "NormalFloat", {bg = "#0E0A23"})
    vim.api.nvim_set_hl(0, "ColorColumn", {bg = "none"})
    vim.api.nvim_set_hl(0, "LineNr", {bg = "none"})

    -- https://github.com/nvim-treesitter/nvim-treesitter?tab=readme-ov-file#highlight
    vim.api.nvim_set_hl(0, 'MyComment', {ctermfg = 79, fg = "#767676"})
    vim.api.nvim_set_hl(0, 'MyFolded',
                        {ctermbg = 70, bg = "#005f5f", fg = "#ffd7af"})
    -- Highlight @foo.bar as "Identifier" only in Lua files
    vim.api.nvim_set_hl(0, "Comment", {link = "MyComment"})
    vim.api.nvim_set_hl(0, "Folded", {link = "MyFolded"})
    -- Folded         xxx ctermfg=59 guifg=#5c6370

    -- CurSearch      xxx ctermfg=0 ctermbg=11 guifg=NvimDarkGrey1 guibg=NvimLightYellow
    vim.api.nvim_set_hl(0, "CurSearch", {
        ctermbg = 70,
        bg = "#d72323",
        fg = "#11cbd7",
        bold = true
    })

    vim.api.nvim_set_hl(0, "QuickFixLine", {
        ctermbg = 70,
        bg = "#d72323",
        fg = "#11cbd7",
        bold = true
    })

    -- плавающие окна
    -- vim.api.nvim_set_hl(0, "FloatBorder", {
    --     ctermbg = 70,
    --     bg = "#d72323",
    --     fg = "#11cbd7",
    --     bold = true
    -- })
    --
    -- рамка между вертикальными окнами
    vim.api.nvim_set_hl(0, "WinSeparator", {ctermbg = 70, fg = "#11cbd7"})

    -- вертикальная полоса для фолдов
    -- hi FoldColumn guibg=#f44336 guifg=#9fc5e8 ctermfg=White ctermbg=Blue term=none cterm=none gui=none
end

SetColor()
