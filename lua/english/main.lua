package.path = package.path .. "/home/stepan/GIT/kn7072/lua/english/?.lua"

local config = require("config")
local functions = require("functions")
local phrasal_verbs = require("phrasal_verbs")
local no_regular_verbs = require("no_regular_verbs")
local kespa = require("kespa")
local question = require("question")

local all_sentense = {}

local no_regular_verbs_table = no_regular_verbs.get_no_regular_verbs()
local phrasal_verbs_table = phrasal_verbs.get_phrasal_verbs()
local kespa_table = kespa.get_kespa()
local question_table = question.get_question()

-- functions.print_table(no_reqular_verbs_table)
-- print(#no_reqular_verbs_table)

-- local all_table_kespa = {}
-- local path_to_kespa =
--     "/home/stepan/GIT/kn7072/EnglishSimulate/Project/кэспа/grammar"
-- local innet_pathes = functions.get_inner_pathes_of_folder(path_to_kespa)
-- for i, dir_i in pairs(innet_pathes) do
--     print(i, dir_i)
--     local lesson_i = functions.get_table_for_dir(dir_i, "rus.txt", "eng.txt",
--                                                  string.format("гив_%d", i))
--     functions.merge_tables(all_table_kespa, lesson_i)
-- end
--
-- local new_shuffle_kespa = functions.shuffle(all_table_kespa)
-- local single_rus_kespa, single_eng_kespa =
--     functions.create_single_lines(new_shuffle_kespa)
-- functions.create_file_for_single_line(
--     "/home/stepan/TEMP/english/кэспа/eng.txt", single_eng_kespa,
--     config.line_size)
-- functions.create_file_for_single_line(
--     "/home/stepan/TEMP/english/кэспа/rus.txt", single_rus_kespa,
--     config.line_size)

-- local path_to_questions =
--     "/home/stepan/GIT/kn7072/EnglishSimulate/Project/Preposition/Questions"
-- local question_table = functions.get_table_for_dir(path_to_questions, "rus.txt",
--                                                    "eng.txt", "ques", true)
-- -- functions.print_table(question_table)
-- local new_shuffle_question_table = functions.shuffle(question_table)
-- -- functions.print_table(new_shuffle_question_table)
--
-- local single_rus, single_eng = functions.create_single_lines(
--                                    new_shuffle_question_table)
-- -- print(single_rus)
-- functions.create_file_for_single_line(
--     "/home/stepan/TEMP/english/question/eng.txt", single_eng, config.line_size)
-- functions.create_file_for_single_line(
--     "/home/stepan/TEMP/english/question/rus.txt", single_rus, config.line_size)

functions.merge_tables(all_sentense, no_regular_verbs_table)
functions.merge_tables(all_sentense, phrasal_verbs_table)
functions.merge_tables(all_sentense, kespa_table)
functions.merge_tables(all_sentense, question_table)
all_sentense = functions.shuffle(all_sentense)

local single_all_sentence_rus, single_all_sentence_eng =
    functions.create_single_lines(all_sentense)
functions.create_file_for_single_line(
    "/home/stepan/TEMP/english/all_sentence_eng.txt", single_all_sentence_eng,
    config.line_size)
functions.create_file_for_single_line(
    "/home/stepan/TEMP/english/all_sentence_rus.txt", single_all_sentence_rus,
    config.line_size)

--[[local table_all_sentence = functions.get_table_for_file(
                               "/home/stepan/GIT/kn7072/ANKI/Предложения.txt")
local single_line_all_sentence = table.concat(table_all_sentence, " ")
print(#table_all_sentence)
-- print(single_line_all_sentence)
functions.create_file_for_single_line("/home/stepan/TEMP/english/all/all.txt",
                                      single_line_all_sentence, config.line_size)
--]]
local all_sentense_mod = require("for_all_sentence")
