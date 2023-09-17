local config = require("config")
local functions = require("functions")
local json = require("json")

local M = {}

local data_no_reg_vords = functions.read_file(config.path_to_no_regular_verbs)
local data_json = json.decode(data_no_reg_vords)

function M.get_no_regular_verbs(prefix)
    local all_table = {}
    prefix = prefix or "no_reg"
    for num_exercise, exersise_val in pairs(data_json) do
        if exersise_val["type"] == "rus_eng" then
            for _, v_sentence in pairs(exersise_val["content"]) do
                all_table[#all_table + 1] = {
                    string.format("(%s)%s_%s", prefix, num_exercise,
                                  v_sentence[1]),
                    string.format("(%s)%s_%s", prefix, num_exercise,
                                  v_sentence[2])
                }
            end
        end
    end

    return all_table
end

return M
