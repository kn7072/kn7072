local config = require("config")
local functions = require("functions")

local M = {}

function M.get_kespa()
    local all_table_kespa = {}
    local innet_pathes = functions.get_inner_pathes_of_folder(
                             config.path_to_dir_kespa)
    for i, dir_i in pairs(innet_pathes) do
        print(i, dir_i)
        local lesson_i = functions.get_table_for_dir(dir_i, "rus.txt",
                                                     "eng.txt", string.format(
                                                         "гив_%d", i))
        functions.merge_tables(all_table_kespa, lesson_i)
    end
    return all_table_kespa
end

return M
