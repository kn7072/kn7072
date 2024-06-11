local api = vim.api
local fn = vim.fn
local M = {}

local cur_window = api.nvim_get_current_win()
local cur_buf = api.nvim_get_current_buf()
local number_win = api.nvim_win_get_number(cur_window)
local win_width_cur = api.nvim_win_get_width(cur_window)
local win_height_cur = api.nvim_win_get_height(cur_window)

function M.get_cursor(win)
    local cur_pos = api.nvim_win_get_cursor(win)
    return cur_pos
end

local function set_mapping()
    local mappings = {q = "close()", ["<cr>"] = "zoom()"}

    for k, v in pairs(mappings) do
        api.nvim_buf_set_keymap(buf, 'n', k,
                                ':lua require"window".' .. v .. '<cr>',
                                {nowait = true, noremap = true, silent = true})
    end

    local other_chars = {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'i', 'n', 'o', 'p', 'r', 's', 't',
        'u', 'v', 'w', 'x', 'y', 'z'
    }
    for _, v in ipairs(other_chars) do
        api.nvim_buf_set_keymap(buf, 'n', v, '',
                                {nowait = true, noremap = true, silent = true})
        api.nvim_buf_set_keymap(buf, 'n', v:upper(), '',
                                {nowait = true, noremap = true, silent = true})
        api.nvim_buf_set_keymap(buf, 'n', '<c-' .. v .. '>', '',
                                {nowait = true, noremap = true, silent = true})
    end

end

function M.close()
    if win and api.nvim_win_is_valid(win) then api.nvim_win_close(win, true) end
end

start_width = nil

function M.zoom()
    local width = api.nvim_win_get_width(win)
    if start_width == nil or width == start_width then
        start_width = width
        api.nvim_win_set_width(win, math.ceil(width * 1.2))
    else
        api.nvim_win_set_width(win, start_width)
    end
end

function M.open_window()
    buf = api.nvim_create_buf(false, true)
    local border_buf = api.nvim_create_buf(false, true)

    local row = math.max(0, math.floor((win_height_cur / 2) - 20))
    local col = math.max(0, math.floor((win_width_cur / 2) - 20))
    local win_width = math.ceil(win_width_cur * 0.5) - 4
    local win_height = math.ceil(win_height_cur * 0.5) - 4

    local border_lines = {'╔' .. string.rep('═', win_width) .. '╗'}
    local middle_line = '║' .. string.rep(' ', win_width) .. '║'
    for i = 1, win_height do table.insert(border_lines, middle_line) end
    table.insert(border_lines, '╚' .. string.rep('═', win_width) .. '╝')
    api.nvim_buf_set_lines(border_buf, 0, -1, false, border_lines)

    local border_opts = {
        win = cur_window,
        -- split = 'left',
        style = "minimal",
        -- relative = "editor",
        relative = "win",
        focusable = false, -- ввод текста не возможен
        width = win_width + 2,
        height = win_height + 2,
        row = row,
        col = col
    }

    local opts = {
        style = "minimal",
        relative = "editor",
        width = win_width,
        height = win_height,
        row = row + 2,
        col = col + 1
    }

    local border_win = api.nvim_open_win(border_buf, true, border_opts)

    win = api.nvim_open_win(buf, true, opts)
    api.nvim_win_set_option(win, 'cursorline', true)
    api.nvim_win_set_option(win, 'wrap', false)

    -- api.nvim_win_set_cursor(win, {5, 5})
    -- local cur_pos = api.nvim_win_get_cursor(0) -- win
    -- api.nvim_buf_set_lines(buf, 0, -1, false, {cur_pos[0] .. cur_pos[1], '', ''})

    api.nvim_buf_set_lines(buf, 0, -1, false,
                           {'#one', '  ' .. 'xxx' .. '  ', '#three'})
    api.nvim_set_option_value('filetype', 'markdown', {buf = buf})
    api.nvim_set_option_value('winhl', 'Normal:BlackOnLightYellow', {win = win})

    set_mapping()

    -- nvim_get_current_line

end

return M
