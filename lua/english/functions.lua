local utf8 = require "lua-utf8"
local M = {}

--- Check if a file or directory exists in this path
local function exists(file)
    local ok, err, code = os.rename(file, file)
    if not ok then
        if code == 13 then
            -- Permission denied, but it exists
            return true, err
        end
    end
    return ok, err
end

--- Check if a directory exists in this path
local function isdir(path)
    -- "/" works on both Unix and Windows
    return exists(path .. "/")
end

local function insert_table(file, table, prefix, add_number)

    if add_number ~= nil then
        for line_i in file:lines("l") do
            -- print(line_i)
            local table_index = #table + 1
            table[table_index] = string.format("(%s)%s%s", prefix,
                                               string.format("%d. ", table_index),
                                               line_i)
        end
    else
        for line_i in file:lines("l") do
            -- print(line_i)
            local table_index = #table + 1
            table[table_index] = string.format("(%s)%s", prefix, line_i)
        end
    end

    return table
end

function M.get_table_for_dir(path_to_dir, rus_file_name, eng_file_name, prefix,
                             add_number)
    local is_dir, err = isdir(path_to_dir)
    print(is_dir, err)
    local res_table = {}
    local rus_table = {}
    local eng_table = {}
    if not is_dir then
        error("Not found dir" .. path_to_dir)
    else
        local path_to_rus_file = path_to_dir .. "/" .. rus_file_name
        local rus_f = assert(io.open(path_to_rus_file, "r"))
        insert_table(rus_f, rus_table, prefix, add_number)

        local path_to_eng_file = path_to_dir .. "/" .. eng_file_name
        local eng_f = assert(io.open(path_to_eng_file, "r"))
        insert_table(eng_f, eng_table, prefix, add_number)

        if #eng_table ~= #rus_table then
            error("count of lines is different" .. "\n" .. path_to_eng_file ..
                      "\n" .. path_to_rus_file)
        end

        for i = 1, #rus_table do
            res_table[#res_table + 1] = {rus_table[i], eng_table[i]}
        end
        return res_table
    end
end

function M.print_table(tab)
    for i, val_i in ipairs(tab) do print(val_i[1], val_i[2]) end
end

function M.shuffle(tab)
    local new_table = {}
    for i = 1, #tab do new_table[i] = tab[i] end
    for i = #tab, 2, -1 do
        local j = math.random(i)
        new_table[i], new_table[j] = new_table[j], new_table[i]
    end
    return new_table
end

function M.create_single_lines(tab)
    local rus_t = {}
    local eng_t = {}
    for _, v in pairs(tab) do
        table.insert(rus_t, v[1])
        table.insert(eng_t, v[2])
    end

    return table.concat(rus_t, " "), table.concat(eng_t, " ")
end

function M.create_file_for_single_line(path_file, line, chunk_size)
    local f = assert(io.open(path_file, "w"))
    for _, line_i in pairs(M:split(line, chunk_size)) do
        f:write(line_i .. "\n")
    end
    -- local i = 1
    -- while true do
    --     local chunk_line = line:sub(i, i + chunk_size - 1)
    --     if true then end
    -- end
end

function M:split(text, chunk_size)
    local s = {}
    local i = 1
    local stop_index = 30

    while true do

        if stop_index < 0 then break end

        local right_border = i + chunk_size - 1
        local line_i = utf8.sub(text, i, right_border)
        -- print(string.format("#### borders %d %d\n", i, right_border))
        if line_i == "" then
            -- строка закончилась - выходим
            break
        end
        local last_character = utf8.len(line_i)
        -- print("line_i " .. line_i)
        local last_char = utf8.sub(line_i, last_character, last_character)
        -- print("last_char " .. last_char)

        if last_char == " " then
            s[#s + 1] = line_i
            -- print(string.format("borders %d %d line_i %s)", i, right_border, line_i))
            -- прибавим к правой границе 1
            i = right_border + 1
        else
            local ofset = 0
            local stop_index_inner = 0
            while true do
                local char_i = utf8.sub(line_i, last_character - ofset,
                                        last_character - ofset)
                -- print("char_i " .. char_i)
                if char_i == " " then
                    break
                else
                    ofset = ofset + 1
                end
                stop_index_inner = stop_index_inner + 1
                if stop_index_inner > 30 then break end
            end
            local new_i = right_border - ofset
            local line_to_save = utf8.sub(text, i, new_i)
            -- print(string.format("borders 2 %d %d line_i %s", i, new_i, line_to_save))
            s[#s + 1] = line_to_save
            i = new_i + 1
        end
        stop_index = stop_index - 1
    end
    return s
end

return M
