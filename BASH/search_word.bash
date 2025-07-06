#!/bin/bash

# set -x
# путь к файлу со всеми словами
path_all_words="/home/stepan/git_repos/kn7072/ANKI/TelegramBot/ALL_WORDS.txt"
# путь к json файлу с примерами
path_to_all_words_json="/home/stepan/git_repos/kn7072/ANKI/TelegramBot/all_words.json"
path_to_synonym="/home/stepan/git_repos/kn7072/ANKI/Синонимы/clear_dict.txt"
word=$(cat ${path_all_words} | awk -F";" '{print $1}' | fzf --tac --tiebreak=index --height=10)
# echo "word ${word}"
command="to_entries[] | select(.key | test(\"^${word}.*\"))"
jq "${command}" "${path_to_all_words_json}"

cat $path_to_synonym | grep -Ei -A 7 --color "${word}"
# set +x
