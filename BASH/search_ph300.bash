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
path_to_file=""

case "$1" in
  "pr")
    echo "phrasal_verbs_300"
    path_to_file=/home/stepan/git_repos/kn7072/EnglishSimulate/Project/PhrasalVerbs/phrasal_verbs_300.json
    jq_key_command="to_entries[] | .key"
    jq_filter="to_entries[] | select(.key | test(\"^%s.*\"))"
    ;;
  "tp")
    echo "preposition of time"
    path_to_file=/home/stepan/git_repos/kn7072/EnglishArticles/preposition/base_time.json
    jq_key_command=".blocks[].items[].phrase_en"
    # jq_filter='.blocks[].items[] | select(.phrase_en == "%s").examples[] | "EN: \(.en)\nRU: \(.ru)\n---"'
    jq_filter='.blocks[] | 
        .category as $cat | 
        .items[] | 
        select(.phrase_en == "%s") as $item | 
        "Категория: \($cat)\nФраза: \($item.phrase_ru)\nПримеры:" | 
        ., ($item.examples[] | "  EN: \(.en)\n  RU: \(.ru)\n---")'
    ;;
  *)
    echo "invalid entry" >&2
    exit 1
    ;;
esac

if file_exists "${path_to_file}"; then
  file_content=$(cat "${path_to_file}")
  key_content=$(echo "${file_content}" | jq -r "${jq_key_command}")
  # echo "${key_content}"
else
  echo "path to file is not valid '${path_to_file}'"
  exit 1
fi

word=$(echo "${key_content}" | awk -F";" '{print $1}' | fzf --tac --tiebreak=index --height=10)
command=$(printf "${jq_filter}" "${word}")

jq -r "${command}" "${path_to_file}"
# echo "${word}"
# echo "${command}"
# echo "${jq_filter}"
# set +x
