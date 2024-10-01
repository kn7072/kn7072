--[[
    If you want to disable debug, just delete that file.
        $tail -F ~/undotree_debug.log
    Run vim, and the log will automatically be appended to the file, and you may watch it using tail:
        $touch ~/undotree_debug.log
    Create a file under $HOME with the name undotree_debug.log
Debug
https://github.com/mbbill/undotree
--]] -- :UndotreeToggle
vim.keymap.set('n', '<leader>&', vim.cmd.UndotreeToggle)
vim.opt.undodir = vim.fn.stdpath('cache') .. '/.undodir'
vim.opt.undofile = true
