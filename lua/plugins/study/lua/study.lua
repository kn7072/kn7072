local api = vim.api
local fn = vim.fn

local M = {}

-- The keycode for the Escape key, used to cancel the window picker.
local escape = 27

local config = {
    -- The characters available for hinting windows.

    -- A group to use for overwriting the Normal highlight group in the floating
    -- window. This can be used to change the background color.
    normal_hl = 'ColorStudyPlugin',

    -- The highlight group to apply to the line that contains the hint characters.
    -- This is used to make them stand out more.
    hint_hl = 'Bold',

    -- The border style to use for the floating window.
    border = 'single'
}

function M.get_all_displayed_buffers()
    local buffers_info = {}
    for _, buf_hndl in ipairs(vim.api.nvim_list_bufs()) do
        if api.nvim_buf_is_loaded(buf_hndl) then
            -- print(api.nvim_buf_get_name(buf_hndl))
            local buffer_name_i = api.nvim_buf_get_name(buf_hndl)
            if buffer_name_i ~= '' then
                buffers_info[buf_hndl] = buffer_name_i
            end
        end
    end
    return buffers_info
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

local function get_char()
    -- https://vimhelp.org/builtin.txt.html
    local ok, char = pcall(fn.getchar)

    return ok and fn.nr2char(char) or nil
end

local function set_mapping(buf)
    local mappings = {q = "close()", ["<cr>"] = "zoom()"}

    for k, v in pairs(mappings) do
        api.nvim_buf_set_keymap(buf, 'n', k,
                                ':lua require".study' .. v .. '<cr>',
                                {nowait = true, noremap = true, silent = true})
    end

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
                           vim.tbl_values(buffers_info))

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
    -- api.nvim_buf_add_highlight(plugin_buffer, 0, 'ColorStudyPluginNew', 0, 3, 7)
    -- api.nvim_buf_add_highlight(plugin_buffer, 0, 'ColorStudyPlugin', 0, 8, 14)

    -- set_mapping()
    -- api.nvim_win_set_option(border_win, 'winhl', 'Normal:' .. config.normal_hl)
    -- api.nvim_win_set_option(border_win, 'diff', false)

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

function M.print_hl()
    print(vim.inspect(api.nvim_get_hl(ns_id, {})))
end

function M.pick()
    local buffers_info = {
        "cterm: cterm attribute map, like highlight-args. If not set, cterm attributes will match those from the attribute map documented above. ",
        "link: name of another highlight group to link to, see :hi-link. ",
        "link: name of another highlight group to link to, see :hi-link. :"
    }

    ns_id = api.nvim_create_namespace("plugin_ns")
    api.nvim_set_hl(ns_id, 'ColorStudyPlugin1', {
        ctermbg = 0,
        fg = '#000000',
        bg = '#7be5c0',
        bold = true,
        italic = true
    })
    vim.notify(string.format("ns_id %s", ns_id), vim.log.levels.DEBUG)

    api.nvim_set_hl(ns_id, 'ColorStudyPluginNew', {
        ctermbg = 0,
        fg = '#000000',
        bg = '#007fff',
        bold = true,
        italic = true
        -- underline = true
    })
    local plugin_buffer = api.nvim_create_buf(false, true)

    local buffers_window = M.open_window(plugin_buffer, buffers_info)

    local used_character = set_mapping(plugin_buffer)

    -- ключевые две строчки - нужно использовать одну из них чтобы стили из пространства ns_id сработали,
    -- после добавления стилей к буферам НЕОБХОДИМО вызвать vim.cmd('redraw')
    -- api.nvim_win_set_hl_ns(buffers_window, ns_id) -- только для указанного окна применяются стили из ns_id
    -- api.nvim_set_hl_ns(ns_id)
    api.nvim_set_hl_ns_fast(ns_id) -- включает для всех окон, применяет стили из ns_id

    api.nvim_buf_add_highlight(0, ns_id, 'ColorStudyPluginNew', 0, 3, 7)
    api.nvim_buf_add_highlight(0, 0, 'ColorStudyPlugin', 0, 8, 14)
    api.nvim_buf_add_highlight(0, ns_id, 'ColorStudyPlugin1', 0, 15, 20)

    api.nvim_buf_add_highlight(plugin_buffer, ns_id, 'ColorStudyPluginNew', 0,
                               3, 7)
    api.nvim_buf_add_highlight(plugin_buffer, ns_id, 'ColorStudyPlugin', 0, 8,
                               14)
    api.nvim_buf_add_highlight(plugin_buffer, ns_id, 'ColorStudyPlugin1', 0, 15,
                               20)
    vim.cmd('redraw')
    local key = get_char()
    api.nvim_buf_clear_namespace(plugin_buffer, 0, 0, -1) -- очистка буфера

    local key = get_char()

    M.close(buffers_window, plugin_buffer)

    vim.notify("msg", vim.log.levels.DEBUG)
end

return M
