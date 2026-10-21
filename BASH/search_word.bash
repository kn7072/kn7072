#!/bin/bash

# set -x
# путь к файлу со всеми словами
path_all_words="/home/stepan/git_repos/kn7072/ANKI/TelegramBot/ALL_WORDS.txt"
# путь к json файлу с примерами
path_to_all_words_json="/home/stepan/git_repos/kn7072/ANKI/TelegramBot/all_words.json"
path_to_synonym="/home/stepan/git_repos/kn7072/ANKI/Синонимы/clear_dict.txt"
word=$(cat ${path_all_words} | awk -F";" '{print $1}' | fzf --tac --tiebreak=index --height=10)

# обрежем пробельные символы в начале и в конеце строки - xargs сделает это втоматически
word=$(echo "${word}" | xargs)
# echo "word ${word}"
# shellcheck disable=SC2016
command='  def pink: "\u001b[38;2;255;0;128m";
  def cyan: "\u001b[38;2;0;255;255m";
  def bold: "\u001b[1m";
  def reset: "\u001b[0m";
  def aquamarine: "\u001b[38;2;127;255;212m";
  def powderblue: "\u001b[38;2;176;224;230m";
  def white: "\u001b[38;2;255;255;255m";
  def beige: "\u001b[38;2;245;245;220m";

  4 as $indent |
  (" " * $indent) as $pad |
  ("---------------------" * $indent) as $ddash |
  ("========" * $indent) as $start_block |

  to_entries[] |
  select(.key == $word) |
  .key as $wordkey |
  .value |
  "\(cyan)\($start_block)\(reset)   \($wordkey)   \(cyan)\($start_block)\(reset)",
  "\n\(powderblue)примеры\(reset)" ,
  (.examples // [] | .[] | ["\(beige)\(.eng)\(reset)", "\(.ru)", ""] | map(if . == "" then . else $pad + . end) | .[]),
   "\(white)\($ddash)\(reset)",
  "\(powderblue)комментарии\(reset) - \(.comment | join(", "))",
  "\(white)\($ddash)\(reset)",
  "\(powderblue)мнемоника\(reset) - \(.mnemonic | join("\n"))",
  "\(white)\($ddash)\(reset)",
 "\(bold)\(aquamarine)\($wordkey)\(reset) \(.transcription)  \(beige)\(.translate)\(reset)"
'
# command="to_entries[] | select(.key | test(\"^${word}.*\"))"
jq -r --arg word "$word" "${command}" "${path_to_all_words_json}"

# cat $path_to_synonym | grep -Ei -A 7 --color "${word}"
exit 0
# set +x
