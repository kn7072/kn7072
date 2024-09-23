local function create_temp_buffer(point, current_buffer)
    local tempfile = vim.fn.tempname()
    vim.notify(string.format("current_buffer %s", current_buffer),
               vim.log.levels.DEBUG)
    vim.cmd.earlier(point)
    local current_buffer_lines = vim.fn.getbufline(current_buffer, 1, "$")
    vim.cmd.later(point)
    if vim.fn.writefile(current_buffer_lines, tempfile) == -1 then
        error("Can not write to temp file: " .. tempfile)
    end
    return tempfile
end

local function get_count_changes()
    -- https://neovim.io/doc/user/builtin.html#undotree()
    return vim.fn.undotree(vim.api.nvim_get_current_buf()).seq_last
end

local function open_dialog_window()
    local count_changing = get_count_changes()
    vim.ui.input({
        prompt = string.format(
            'Enter number of hishory changing from 1 to %s: ', count_changing)
    }, function(input)
        local number_changing = tostring(input)
        return number_changing
    end)
end

local current_buffer = vim.api.nvim_get_current_buf()
local path_to_file = create_temp_buffer(0, current_buffer)
vim.notify(path_to_file, vim.log.levels.DEBUG)

local chosen_number = open_dialog_window()
local path_to_file_h = create_temp_buffer(chosen_number, current_buffer)
vim.notify(path_to_file_h, vim.log.levels.DEBUG)

vim.opt.diffopt:append("vertical")
vim.cmd.diffs(path_to_file_h)
