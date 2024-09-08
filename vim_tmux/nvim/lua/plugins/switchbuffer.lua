local nvim_win = require('switch_buffer')
vim.api.nvim_set_hl(0, 'BlackOnLightYellowBuffer',
                    {ctermbg = 0, fg = '#000000', bg = '#e5c07b', bold = true})

nvim_win.setup({
    -- The characters available for hinting windows.
    chars = {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    },

    -- A group to use for overwriting the Normal highlight group in the floating
    -- window. This can be used to change the background color.
    normal_hl = 'BlackOnLightYellowBuffer',

    -- The highlight group to apply to the line that contains the hint characters.
    -- This is used to make them stand out more.
    hint_hl = 'Bold',

    -- The border style to use for the floating window.
    border = 'single'
})

vim.keymap.set('n', '<leader>b', require('switch_buffer').pick)
