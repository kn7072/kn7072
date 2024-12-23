local api = vim.api
local fn = vim.fn

local M = {}

-- The keycode for the Escape key, used to cancel the window picker.
local escape = 27

local config = {
    -- The characters available for hinting windows.
    chars = {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    },

    -- A group to use for overwriting the Normal highlight group in the floating
    -- window. This can be used to change the background color.
    normal_hl = 'Normal',

    -- The highlight group to apply to the line that contains the hint characters.
    -- This is used to make them stand out more.
    hint_hl = 'Bold',

    -- The border style to use for the floating window.
    border = 'single'
}

function M.get_all_displayed_buffers()
    local buffers_info = {}
    for _, buf_hndl in ipairs(vim.api.nvim_list_bufs()) do
        if api.nvim_buf_is_loaded(buf_hndl) and vim.bo[buf_hndl].buflisted then
            -- print(api.nvim_buf_get_name(buf_hndl))
            local buffer_name_i = fn.fnamemodify(
                                      api.nvim_buf_get_name(buf_hndl), ":t")
            if buffer_name_i ~= '' then
                buffers_info[buf_hndl] = buffer_name_i
            end
        end
    end
    return buffers_info
end

function M.get_size_window()

end

local function get_char()
    -- https://vimhelp.org/builtin.txt.html
    local ok, char = pcall(fn.getchar)

    return ok and fn.nr2char(char) or nil
end

function spairs(t, order)
    -- collect the keys
    local keys = {}
    for k in pairs(t) do
        keys[#keys + 1] = k
    end

    -- if order function given, sort by it by passing the table and keys a, b,
    -- otherwise just sort the keys 
    if order then
        table.sort(keys, function(a, b)
            return order(t, a, b)
        end)
    else
        table.sort(keys)
    end

    -- return the iterator function
    local i = 0
    return function()
        i = i + 1
        if keys[i] then
            return keys[i], t[keys[i]]
        end
    end
end

local fun_order = function(t, a, b)
    return t[b] > t[a]
end

local function set_mapping(buf, buffers_info)
    local mappings = {q = "close()", ["<cr>"] = "zoom()"}
    local buffers_maps = {}

    for k, v in pairs(mappings) do
        api.nvim_buf_set_keymap(buf, 'n', k,
                                ':lua require"switch_buffer".' .. v .. '<cr>',
                                {nowait = true, noremap = true, silent = true})
    end

    local other_chars = {
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'i', 'n', 'o', 'p', 'r', 's', 't',
        'u', 'v', 'w', 'x', 'y', 'z'
    }
    local char_index = 1
    for buff_hd, buff_name in spairs(buffers_info, fun_order) do
        local current_char = other_chars[char_index]
        buffers_maps[current_char] = buff_hd
        local row = string.format("%s %s", other_chars[char_index], buff_name)
        buffers_info[buff_hd] = row
        char_index = char_index + 1
    end

    -- for _, v in ipairs(other_chars) do
    --     api.nvim_buf_set_keymap(buf, 'n', v, '',
    --                             {nowait = true, noremap = true, silent = true})
    --     api.nvim_buf_set_keymap(buf, 'n', v:upper(), '',
    --                             {nowait = true, noremap = true, silent = true})
    --     api.nvim_buf_set_keymap(buf, 'n', '<c-' .. v .. '>', '',
    --                             {nowait = true, noremap = true, silent = true})
    -- end
    return buffers_maps
end

function M.get_buffer_name()

end

local function prepare_table_for_show(tbl)
    local tbl_for_show = {}
    for _, buff_name in spairs(tbl, fun_order) do
        table.insert(tbl_for_show, string.format("%s", buff_name))
    end
    return tbl_for_show
end

local function get_max_length(tbl)
    local max_length_buffer_name = -1
    for _, buffer_name_i in pairs(tbl) do
        -- https://stackoverflow.com/questions/43125333/lua-string-length-cyrillic-in-utf8
        local len_buffer_name = #(buffer_name_i):gsub('[\128-\191]', '')
        if len_buffer_name > max_length_buffer_name then
            max_length_buffer_name = len_buffer_name
        end
    end
    return max_length_buffer_name
end

function M.open_window(plugin_buffer, buffers_info)
    -- local buf = api.nvim_create_buf(false, true)
    -- local plugin_buffer = api.nvim_create_buf(false, true)

    -- выбирать наибольшее окно если в текущее не помещается информация
    local current_win = api.nvim_get_current_win()
    local current_win_width = api.nvim_win_get_width(current_win)
    local current_win_height = api.nvim_win_get_height(current_win)

    local window_width = get_max_length(buffers_info) + 1
    local count_row = #vim.tbl_values(buffers_info)
    -- local border_lines = {'╔' .. string.rep('═', window_width) .. '╗'}
    -- local middle_line = '║' .. string.rep(' ', window_width) .. '║'
    -- for i = 1, count_row do
    --     table.insert(border_lines, middle_line)
    -- end
    -- table.insert(border_lines, '╚' .. string.rep('═', window_width) .. '╝')
    -- api.nvim_buf_set_lines(plugin_buffer, 0, -1, false, border_lines)
    api.nvim_buf_set_lines(plugin_buffer, 0, -1, false,
                           prepare_table_for_show(buffers_info)) -- vim.tbl_values(buffers_info)

    local window_opt = {
        win = current_win,
        -- split = 'left',
        style = "minimal",
        border = {"╔", "═", "╗", "║", "╝", "═", "╚", "║"},
        -- relative = "editor",
        relative = "win",
        focusable = false, -- ввод текста не возможен
        width = window_width + 0,
        height = count_row + 0,
        row = 1,
        col = 5
    }

    local border_win = api.nvim_open_win(plugin_buffer, false, window_opt)
    -- set_mapping()
    api.nvim_win_set_option(border_win, 'winhl', 'Normal:' .. config.normal_hl)
    api.nvim_win_set_option(border_win, 'diff', false)

    -- We need to redraw here, otherwise the floats won't show up
    vim.cmd('redraw')
    return border_win
end

function M.close(window, buffer)
    api.nvim_win_close(window, true)
    api.nvim_buf_delete(buffer, {force = true})
end

-- Configures the plugin by merging the given settings into the default ones.
function M.setup(user_config)
    config = vim.tbl_extend('force', config, user_config)
end

function M.pick()
    buffers_info = M.get_all_displayed_buffers()
    local plugin_buffer = api.nvim_create_buf(false, true)

    local used_character = set_mapping(plugin_buffer, buffers_info)
    local buffers_window = M.open_window(plugin_buffer, buffers_info)
    local key = get_char()

    local chosen_buffer = vim.tbl_get(used_character, key)
    if chosen_buffer then
        api.nvim_set_current_buf(chosen_buffer)
    end

    local window = nil
    if not key or key == escape then
        M.close(buffers_window, plugin_buffer)
        return
    end

    -- -- if key == "a" then
    --     M.close(buffers_window, plugin_buffer)
    -- end
    M.close(buffers_window, plugin_buffer)
end

return M
