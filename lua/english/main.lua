package.path = package.path .. "/home/stepan/GIT/kn7072/lua/english/?.lua"

local config = require("config")
-- print(config.path_to_general_dir)
local functions = require("functions")

local path_to_questions =
    "/home/stepan/GIT/kn7072/EnglishSimulate/Project/Preposition/Questions"
local question_table = functions.get_table_for_dir(path_to_questions, "rus.txt",
                                                   "eng.txt", "qus", true)
functions.print_table(question_table)

local new_shuffle_question_table = functions.shuffle(question_table)
functions.print_table(new_shuffle_question_table)

local single_rus, single_eng = functions.create_single_lines(
                                   new_shuffle_question_table)
print(single_rus)
