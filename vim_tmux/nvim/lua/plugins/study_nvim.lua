local nvim_win = require('study')
vim.api.nvim_set_hl(0, 'ColorStudyPlugin',
                    {ctermbg = 0, fg = '#000000', bg = '#e5c07b', bold = true})

-- vim.api.nvim_set_hl(0, 'ColorStudyPluginNew',
--                     {ctermbg = 0, fg = '#000000', bg = '#007fff', bold = true})

nvim_win.setup({

    -- A group to use for overwriting the Normal highlight group in the floating
    -- window. This can be used to change the background color.
    normal_hl = 'ColorStudyPlugin',

    -- The highlight group to apply to the line that contains the hint characters.
    -- This is used to make them stand out more.
    hint_hl = 'Bold',

    -- The border style to use for the floating window.
    border = 'single'
})

vim.keymap.set('n', '<leader>r', require('study').pick)
