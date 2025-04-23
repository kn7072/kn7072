--[[
The Lua programming offers a set of metacharacters, special sequence and sets which have a special meaning as listed below:

    . – : This is a metacharacter which matches all characters.
    %a: This is a special sequence which matches all letters.
    %l: This is a special sequence which matches all lowercase letters.
    %u: This is a special sequence which matches all uppercase letters.
    %d: This is a special sequence which matches all digits.
    %s: This is a special sequence which matches all whitespace characters.
    %x: This is a special sequence which matches all hexadecimal digits.
    %p: This is a special sequence which matches all punctuation characters.
    %g: This is a special sequence which matches all printable characters except space.
    %c: This is a special sequence which matches all control characters.
    [set]: This is a set which matches the class which is the union of all characters in set.
    [^set]: This is a special sequence which matches the complement of set.
    +: This is a greedy match which matches 1 or more occurrences of previous character class.
    *: This is a greedy match which matches 0 or more occurrences of previous character class.
    ?: This is a match exactly which matches 0 or 1 occurrence of previous character class.
    – -: This is a lazy match which matched 0 or more occurrences of previous character class.
]]

local data = "Name: John, Age: 25"
local name, age = data:match("Name: (%w+), Age: (%d+)")
print(name, age)

local text = [[/home/stepan/git_repos/kn7072/ANKI/TelegramBot/create_file_for_anki_new.py:341:1: E101 indentation contains mixed spaces and tabs]]
local text = [[/home/stepan/git_repos/kn7072/ANKI/TelegramBot/create_file_for_anki_new.py:341:1: E101]]
-- /home/stepan/git_repos/kn7072/ANKI/TelegramBot/create_file_for_anki_new.py:342:1: W191 indentation contains tabs
-- /home/stepan/git_repos/kn7072/ANKI/TelegramBot/create_file_for_anki_new.py:342:1: E101 indentation contains mixed spaces and tabs
-- /home/stepan/git_repos/kn7072/ANKI/TelegramBot/create_file_for_anki_new.py:343:1: W191 indentation contains t
-- /home/stepan/git_repos/kn7072/ANKI/TelegramBot/create_file_for_anki_new.py:343:1: E101 indentation contains m
-- /home/stepan/git_repos/kn7072/ANKI/TelegramBot/create_file_for_anki_new.py:344:1: W191 indentation contains t
-- /home/stepan/git_repos/kn7072/ANKI/TelegramBot/create_file_for_anki_new.py:344:1: E101 indentation contains m
-- /home/stepan/git_repos/kn7072/ANKI/TelegramBot/create_file_for_anki_new.py:345:1: W191 indentation contains t
-- /]]

-- local pattern = [[(.*)?:(%d+):(%d+)(.*)]]
-- local pattern = [[:(%d+):(%d+)(.*)]]
-- local groups = { "row", "col", "message" }

local pattern = [[(%g+):(%d+):(%d+): ([%w%d]+)]]
local groups = { "filename", "row", "col", "code", "message" }
local filename, row, col, message = text:match(pattern)
print(filename, row, col, message)

local text = [[/home/stepan/git_repos/kn7072/ANKI/TelegramBot/create_file_for_anki_new.py:341:1:]]
local pattern = [[(%g+):(%d+):(%d+):]]
local groups = { "filename", "row", "col"}
local filename, row, col = text:match(pattern)
print(filename, row, col)

local text = [[/home/stepan/xit_repos/kn7072/ANKI/TelegramBot/create_file_for_anki_new.py:341:1:]]
local text = [[khomekstepankxit_reposkknkANKIkTelegramBotkcreate]]
local pattern = [[(%g+)]]
local pattern = "([%g]+)"
local groups = { "filename", "row", "col"}
local filename, row, col = text:match(pattern)
print(text, pattern, filename, row, col)


local text = [[E101]]
local pattern = [[(%w%d+)]]
local code= text:match(pattern)
print("code ", code)

