local config = require("config")
local json = require("json")
local functions = require("functions")
local M = {}

local data_phrasal_verbs = functions.read_file(
                               config.path_to_exercise_phrasal_verbs)
local json_data = json.decode(data_phrasal_verbs)

function M.get_phrasal_verbs()
    local all_table = {}
    for num_exercise, v_exercise in pairs(json_data) do
        -- print(num_exercise)
        for _, v_sentence in pairs(v_exercise) do
            all_table[#all_table + 1] = {
                string.format("%s_%s", num_exercise, v_sentence[1]),
                string.format("%s_%s", num_exercise, v_sentence[2])
            }
        end
    end
    return all_table
end

return M
