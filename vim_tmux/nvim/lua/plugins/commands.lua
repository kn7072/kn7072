local api = vim.api
local open = io.open

-- see if the file exists
function file_exists(file)
    local f = io.open(file, "rb")
    if f then
        f:close()
    end
    return f ~= nil
end

function lines_from(file)
    if not file_exists(file) then
        return {}
    end
    local lines = {}
    for line in io.lines(file) do
        lines[#lines + 1] = line
    end
    return lines
end

local function read_file(path)

    if not file_exists(path) then
        return nil
    end

    local file = open(path, "rb") -- r read mode and b binary mode
    if not file then
        return nil
    end
    local content = file:read "*a" -- *a or *all reads the whole file
    file:close()
    return content
end

api.nvim_create_user_command('Flake8', function(opts)
    local cmd = "flake8"
    -- print("flake8")
    if vim.fn.executable(cmd) then
        -- print("flake8", opts.args)
        cmd = string.format("%s %s", cmd, opts.args)
        -- print(vim.fn.system(cmd))

        local output = vim.split(vim.trim(vim.fn.system(cmd)), "\n")
        print(vim.inspect(output))
        return output
    end

end, {desc = 'First flake8', nargs = 1, bang = true})

api.nvim_create_user_command('Upper', function(opts)
    local current_word = vim.fn.expand("<cword>")
    local current_word_upper = string.upper(current_word)
    vim.cmd("normal! diwi" .. current_word_upper)
end, {})

api.nvim_create_user_command('SnakeCase', function(opts)
    local current_word = vim.fn.expand("<cword>")
    -- change case to snake case
    local snake_case = current_word:gsub("(%u)", "_%1"):gsub("(%u)",
                                                             string.lower):gsub(
                           "^_", "")
    vim.cmd("normal! diwi" .. snake_case)
end, {})

api.nvim_create_user_command('ToggleCase', function(opts)
    local current_word = vim.fn.expand("<cword>")
    if current_word:match("_") then
        vim.cmd("CamalCase")
    else
        vim.cmd("SnakeCase")
    end
end, {})

api.nvim_create_user_command('CamalCase', function(opts)
    local current_word = vim.fn.expand("<cword>")
    -- change case to camal case
    local camal_case = current_word:gsub("_(.)", string.upper):gsub("^(.)",
                                                                    string.upper)
    vim.cmd("normal! diwi" .. camal_case)
end, {})

api.nvim_create_user_command('Tags', function(opts)
    local cursor_word = vim.fn.expand("<cword>")
    print(cursor_word)
    print(vim.inspect(vim.fn.taglist(string.format("^%s", cursor_word))))
end, {desc = "Find tags"})

vim.api.nvim_create_user_command('Upper2', function(opts)
    print(opts.args)
end, {
    nargs = 1,
    complete = function(ArgLead, CmdLine, CursorPos)
        -- return completion candidates as a list-like table
        return {'foo', 'bar', 'baz'}
    end
})

api.nvim_create_user_command('Test', function(opts)
    -- print(string.upper(opts.args))
    print("xxxx")
    api.nvim_set_hl(0, "FoldColumn",
                    {ctermbg = 70, bg = "#d72323", fg = "#11cbd7", bold = true})
end, {})

local function split(str, sep)
    local result = {}
    local regex = ("([^%s]+)"):format(sep)
    for each in str:gmatch(regex) do
        local res, _ = each:gsub("\n", "")
        table.insert(result, res)
    end
    return result
end

local eng_win_id = -1
local bufnr = -1
local data_files_table = {}

local function get_data_file(file_path)
    local data_file = data_files_table[file_path]
    if not data_file then
        local file_content = read_file(file_path)
        if file_content == nil then
            error(string.format("file %s not found", file_path))
        end
        data_file = file_content
        data_files_table[file_path] = file_content
    end
    return data_file
end

api.nvim_create_user_command('Eng', function(opts)
    -- local cmd = string.format(
    --                 [[' | jq 'to_entries[] | select(.key | test("%s.*"))']],
    --                 opts.args)
    -- print(opts.args)

    -- local file_path = "/home/stepan/temp/саша/json"
    local file_path =
        "/home/stepan/git_repos/kn7072/ANKI/TelegramBot/all_words.json"
    local path_to_synonym =
        "/home/stepan/git_repos/kn7072/ANKI/Синонимы/clear_dict.txt"
    local cmd_for_all_words = string.format(
                                  [[jq 'to_entries[] | select(.key | test("^%s.*"))' "%s"]],
                                  opts.args, file_path)
    local cmd_for_synonym = string.format(
                                [[cat "%s" | grep -Ei -A 7 --color "%s"]],
                                path_to_synonym, opts.args)

    -- local cmd_for_all_words = string.format(
    --                 [[cat %s | jq 'to_entries[] | select(.key | test("%s.*"))']],
    --                 file_path, opts.args)

    -- print(cmd_for_all_words)
    -- local file_content = read_file(file_path)
    -- local file_content = get_data_file(file_path)
    -- local lines = lines_from(file_path)

    -- if file_content == nil then
    --     print(string.format("file %s not found", file_path))
    -- end
    -- print(file_content)
    -- print("echo '" .. file_content .. cmd_for_all_words)
    -- local bufnr = api.nvim_get_current_buf()
    --
    --
    -- local content_word = vim.fn.system("echo '" .. file_content .. cmd_for_all_words)
    local content_word = vim.fn.system(cmd_for_all_words)
    -- print(content_word)

    local content_synonym = vim.fn.system(cmd_for_synonym)
    content_word = content_word .. content_synonym

    local current_win = api.nvim_get_current_win()
    local current_win_width = api.nvim_win_get_width(current_win)
    local current_win_height = api.nvim_win_get_height(current_win)

    if not api.nvim_buf_is_valid(bufnr) then
        bufnr = api.nvim_create_buf(false, true)
        -- print(string.format("%s", bufnr))
        api.nvim_buf_set_name(bufnr, 'English')

    end
    -- local bufnr = api.nvim_create_buf(false, true)
    -- print(string.format("%s", bufnr))
    -- api.nvim_buf_set_name(bufnr, 'English')

    local lines = split(content_word, "\n")
    -- for _, line in ipairs(lines) do
    --     print(line)
    -- end

    -- lines = {"xxx", "yyyy"}
    -- api.nvim_buf_set_text(bufnr, 0, 0, 0, 0, lines)
    local count_lines = api.nvim_buf_line_count(bufnr)

    -- api.nvim_buf_set_lines(bufnr, 0, 0, false, lines) -- если необходимо продолжить писать в тот же буфер
    api.nvim_buf_set_lines(bufnr, 0, count_lines, false, lines)
    --
    -- local window_opt = {
    --     win = current_win,
    --     -- split = 'left',
    --     style = "minimal",
    --     border = {"╔", "═", "╗", "║", "╝", "═", "╚", "║"},
    --     -- relative = "editor",
    --     relative = "win",
    --     focusable = false, -- ввод текста не возможен
    --     width = current_win_width,
    --     height = current_win_height,
    --     row = 1,
    --     col = 5
    -- }
    if not api.nvim_win_is_valid(eng_win_id) then
        local window_opt = {win = current_win, split = 'right'} -- , split = 'left'
        eng_win_id = api.nvim_open_win(bufnr, false, window_opt) -- window_opt
    end

    api.nvim_set_current_win(eng_win_id)

    -- print(eng_win_id)
    vim.cmd('redraw')

    -- print(type(content_word))

    -- print(vim.fn.executable("echo '" .. file_content .. cmd_for_all_words))

end, {desc = "English", nargs = 1})
