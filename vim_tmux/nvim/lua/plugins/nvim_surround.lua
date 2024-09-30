local ok, surround = pcall(require, 'surround')

if not ok then
    error(string.format("Error require %s", surround))
else
    -- print(string.format("m %s", vim.inspect(surround)))
end

local delimiter = "|"
surround.setup(delimiter)
vim.keymap.set('v', 'ii', require('surround').open)
