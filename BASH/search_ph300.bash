#!/bin/bash

## Function to check if a file exists
## Returns 0 if file exists, 1 if it doesn't
file_exists() {
  if [[ -f "$1" ]]; then
    return 0
  else
    return 1
  fi
}

# set -x
# path_to_file=~/EnglishSimulate/Project/PhrasalVerbs/phrasal_verbs_300.json
path_to_file=/home/stepan/git_repos/kn7072/EnglishSimulate/Project/PhrasalVerbs/phrasal_verbs_300.json

if file_exists "${path_to_file}"; then
  file_content=$(cat "${path_to_file}")
  key_content=$(echo "${file_content}" | jq -r 'to_entries[] | .key')
  # echo "${key_content}"
else
  echo "Failed path to file ${path_to_file}"
  exit 1
fi

# while true; do
#   read input=$(echo "${key_content}" | awk -F";" '{print $1}' | fzf --tac --tiebreak=index --height=10)
#
word=$(echo "${key_content}" | awk -F";" '{print $1}' | fzf --tac --tiebreak=index --height=10)
command="to_entries[] | select(.key | test(\"^${word}.*\"))"
jq "${command}" "${path_to_file}"
# done
# set +x
