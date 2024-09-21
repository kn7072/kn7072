local api = vim.api
local fn = vim.fn

local M = {}

function M.get_lines_visual_selection()
    -- https://neovim.io/doc/user/builtin.html#getpos()
    -- vim.cmd("normal V")
    -- https://github.com/neovim/neovim/issues/19770
    api.nvim_feedkeys('\027', 'xt', false)
    -- vim.notify(string.format("cursor %s",
    --                          vim.inspect(api.nvim_win_get_cursor(0))),
    --            vim.log.levels.DEBUG)
    local mode = fn.mode()
    local visualmode = fn.visualmode()

    vim.notify(type(visualmode), vim.log.levels.DEBUG)
    vim.notify(visualmode, vim.log.levels.DEBUG)
    if visualmode == "V" then
        vim.notify(string.format("mode V"))
    elseif visualmode == "n" then
        vim.notify(string.format("mode n"))
    elseif visualmode == vim.fn.nr2char(0x16) then
        vim.notify(string.format("mode ^v"))
    else
        vim.notify(string.format("mode x %s", visualmode))
        vim.notify(visualmode)
    end
    -- vim.notify(visualmode, vim.log.levels.DEBUG)
    -- vim.notify(vim.inspect(api.nvim_get_mode()), vim.log.levels.DEBUG)

    local start_pos = fn.getpos("'<")
    local end_pos = fn.getpos("'>")
    vim.notify("stert_pos" .. vim.inspect(start_pos), vim.log.levels.DEBUG)
    vim.notify("end_pos" .. vim.inspect(end_pos), vim.log.levels.DEBUG)

    local n_lines = math.abs(end_pos[2] - start_pos[2]) + 1
    local lines = api.nvim_buf_get_lines(0, start_pos[2] - 1, end_pos[2], false)

    -- vim.notify(table.concat(lines, '\n'), vim.log.levels.DEBUG)

    lines[1] = string.sub(lines[1], start_pos[3], -1)
    if n_lines == 1 then
        lines[n_lines] = string.sub(lines[n_lines], 1,
                                    end_pos[3] - start_pos[3] + 1)
    else
        lines[n_lines] = string.sub(lines[n_lines], 1, end_pos[3])
    end

    return {lines = lines, start_pos = start_pos, end_pos = end_pos}
end

local function surround_text_block(lines_list, start_text, end_text)
    local surround_table = {start_text}
    -- return string.format("%s\n%s\n%s", start_text,
    --                      table.concat(lines_list, '\n'), end_text)
    vim.list_extend(surround_table, lines_list)
    table.insert(surround_table, end_text)
    return surround_table
end

local function delete_visual_block()

end

local function set_text(text, start_pos, end_pos)
    --[[
    nvim_buf_set_text({buffer}, {start_row}, {start_col}, {end_row}, {end_col}, {replacement}) Sets (replaces) a range in the buffer
    ]]

    vim.notify("stert_pos" .. vim.inspect(start_pos), vim.log.levels.DEBUG)
    vim.notify("end_pos" .. vim.inspect(end_pos), vim.log.levels.DEBUG)
    vim.notify("test " .. table.concat(text, '\n'), vim.log.levels.DEBUG)
    api.nvim_buf_set_text(0, start_pos[2] - 1, start_pos[3] - 1, end_pos[2] - 1,
                          end_pos[3] - 1, {text}) -- {"xxx", "yyyy"}{text}
end
-- vim.notify(vim.inspect(get_visual_selection()), vim.log.levels.DEBUG)
function M:open()
    vim.ui.input({prompt = 'enter block: '}, function(input)
        local block = tostring(input)
        vim.notify(string.format("\n%s\n", block), vim.log.levels.DEBUG)

        local lines_table = M.get_lines_visual_selection()

        local surrounded_table = surround_text_block(lines_table.lines, block,
                                                     block)
        vim.notify(string.format("\n%s\n", vim.inspect(surrounded_table)),
                   vim.log.levels.DEBUG)

        set_text(surrounded_table, lines_table.start_pos, lines_table.end_pos)
        return ""

    end)
end

function M.setup()

end

return M
