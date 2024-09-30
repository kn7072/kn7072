local api = vim.api
local fn = vim.fn

local M = {}

local function splitString(input, delimiter)
    local result = {}
    local pattern = string.format("([^%s]+)", delimiter)
    for word in string.gmatch(input, pattern) do
        table.insert(result, word)
    end
    return result
end

local function get_mode()
    -- local mode = fn.mode()
    local visualmode = fn.visualmode()

    -- vim.notify(type(visualmode), vim.log.levels.DEBUG)
    -- vim.notify(visualmode, vim.log.levels.DEBUG)
    if visualmode == "V" then
        -- vim.notify(string.format("mode V"))
    elseif visualmode == "n" then
        -- vim.notify(string.format("mode n"))
    elseif visualmode == vim.fn.nr2char(0x16) then
        -- vim.notify(string.format("mode ^v"))
        visualmode = "^v"
    else
        -- vim.notify(string.format("mode x %s", visualmode))
        -- vim.notify(visualmode)
    end
    return visualmode

end

local function set_lines_normal(start_pos, end_pos, surround_table)
    local num_line_start = start_pos[2] - 1
    local num_col_start = start_pos[3] - 1
    local num_line_end = end_pos[2] - 1
    local num_col_end = end_pos[3] - 1
    local current_buffer = api.nvim_get_current_buf()
    if num_line_start == num_line_end then
        local shosen_text = api.nvim_buf_get_text(current_buffer,
                                                  num_line_start, num_col_start,
                                                  num_line_start, num_col_end,
                                                  {})
        api.nvim_buf_set_text(current_buffer, num_line_start, num_col_start,
                              num_line_start, num_col_end, {
            string.format("%s%s%s", surround_table[1], shosen_text[1],
                          surround_table[2])
        })
    else
        api.nvim_buf_set_text(current_buffer, num_line_start, num_col_start,
                              num_line_start, num_col_start, {surround_table[1]})

        api.nvim_buf_set_text(current_buffer, num_line_end, num_col_end,
                              num_line_end, num_col_end, {surround_table[2]})
    end
end

local function set_lines_shift_v(start_pos, end_pos, surround_table)
    local num_line_start = start_pos[2] - 1
    local num_line_end = end_pos[2] + 1
    local current_buffer = api.nvim_get_current_buf()
    api.nvim_buf_set_lines(current_buffer, num_line_start, num_line_start,
                           false, {surround_table[1]})
    api.nvim_buf_set_lines(current_buffer, num_line_end, num_line_end, false,
                           {surround_table[2]})
end

local function set_lines_block_v(start_pos, end_pos, surround_table)
    local num_line_start = start_pos[2] - 1
    local num_line_end = end_pos[2] - 1
    local num_col_start = start_pos[3] - 1
    local num_col_end = end_pos[3] + end_pos[4]
    local count_line = num_line_end - num_line_start
    local current_buffer = api.nvim_get_current_buf()
    -- vim.notify(string.format("%s", count_line), vim.log.levels.DEBUG)
    for i = 0, count_line do
        local current_line = num_line_start + i
        local shosen_text = api.nvim_buf_get_text(current_buffer, current_line,
                                                  num_col_start, current_line,
                                                  num_col_end, {})
        if shosen_text[1] ~= "" then
            -- vim.notify(vim.inspect(shosen_text), vim.log.levels.DEBUG)
            api.nvim_buf_set_text(current_buffer, current_line, num_col_start,
                                  current_line, num_col_end, {
                string.format("%s%s%s", surround_table[1], shosen_text[1],
                              surround_table[2])
            })
        end
    end
end

local function surround_text_block(surround_table)
    api.nvim_feedkeys('\027', 'xt', false)

    local mode = get_mode()
    local start_pos = fn.getpos("'<")
    local end_pos = fn.getpos("'>")
    -- vim.notify("stert_pos" .. vim.inspect(start_pos), vim.log.levels.DEBUG)
    -- vim.notify("end_pos" .. vim.inspect(end_pos), vim.log.levels.DEBUG)

    if mode == "v" then
        set_lines_normal(start_pos, end_pos, surround_table)
        -- vim.notify("end_v", vim.log.levels.DEBUG)
    elseif mode == "V" then
        set_lines_shift_v(start_pos, end_pos, surround_table)
        -- vim.notify("end_V", vim.log.levels.DEBUG)
    elseif mode == "^v" then
        set_lines_block_v(start_pos, end_pos, surround_table)
        -- vim.notify("end_^v", vim.log.levels.DEBUG)
    else

    end
end

function M:open()
    vim.ui.input({prompt = 'enter block: '}, function(input)
        local block = tostring(input)
        local surround_table = splitString(block, M.delimiter)
        if #surround_table == 1 then
            surround_table[2] = block
        end
        -- vim.notify(string.format("\n%s\n", block), vim.log.levels.DEBUG)
        surround_text_block(surround_table)
    end)
end

function M.setup(delimiter)
    M.delimiter = delimiter
end

return M
