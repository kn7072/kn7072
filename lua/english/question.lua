local config = require("config")
local functions = require("functions")

local M = {}

function M.get_question()
    local question_table = functions.get_table_for_dir(config.path_to_questions,
                                                       "rus.txt", "eng.txt",
                                                       "ques", true)
    return question_table
end

return M
