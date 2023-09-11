package.path = package.path .. "/home/stepan/GIT/kn7072/lua/english/?.lua"

local config = require("config")
-- print(config.path_to_general_dir)
local functions = require("functions")

local path_to_questions =
    "/home/stepan/GIT/kn7072/EnglishSimulate/Project/Preposition/Questions"
local question_table = functions.get_table_for_dir(path_to_questions, "rus.txt",
                                                   "eng.txt", "qus", true)
-- functions.print_table(question_table)

local new_shuffle_question_table = functions.shuffle(question_table)
-- functions.print_table(new_shuffle_question_table)

local single_rus, single_eng = functions.create_single_lines(
                                   new_shuffle_question_table)
-- print(single_rus)
functions.create_file_for_single_line(
    "/home/stepan/TEMP/english/question/eng.txt", single_eng, config.line_size)
functions.create_file_for_single_line(
    "/home/stepan/TEMP/english/question/rus.txt", single_rus, config.line_size)

local table_all_sentence = functions.get_table_for_file(
                               "/home/stepan/GIT/kn7072/ANKI/Предложения.txt")
local single_line_all_sentence = table.concat(table_all_sentence, " ")
print(#table_all_sentence)
-- print(single_line_all_sentence)
functions.create_file_for_single_line("/home/stepan/TEMP/english/all/all.txt",
                                      single_line_all_sentence, config.line_size)
