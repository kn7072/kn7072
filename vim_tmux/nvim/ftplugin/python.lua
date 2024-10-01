vim.opt_local.fillchars:append({fold = ' '})

function myfoldtext()
    local line = vim.fn.getline(vim.v.foldstart)
    return string.format("%s %s ( lines: %s ):...", '+-- ', line,
                         (vim.v.foldend - vim.v.foldstart + 1))
end

vim.opt_local.foldtext = 'v:lua.myfoldtext()'
