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
    # shellcheck disable=SC2016

    # jq_filter="to_entries[] | select(.key | test(\"^%s.*\"))"
    jq_filter='
      def pink: "\u001b[38;2;255;0;128m";
      def cyan: "\u001b[38;2;0;255;255m";
      def bold: "\u001b[1m";
      def reset: "\u001b[0m";
      def aquamarine: "\u001b[38;2;127;255;212m";
      def powderblue: "\u001b[38;2;176;224;230m";
      def white: "\u001b[38;2;255;255;255m";
      def beige: "\u001b[38;2;245;245;220m";
      def mate: "\u001b[38;2;189;236;182m";

      4 as $indent |
      (" " * $indent) as $pad |
      ("-" * 21) as $ddash |
      ("========" * $indent) as $start_block |


      to_entries[] |
      select(.key == $word) |
      .key as $wordkey |
      .value as $val |

      # 1. Заголовок со словом
      "\(cyan)\($start_block)\(reset)   \($wordkey)   \(cyan)\($start_block)\(reset)",
      "\(bold)\(aquamarine)\($wordkey)\(reset) \(beige)(\($val.grammar))\(reset)",
      "\(white)\($ddash)\(reset)",

      # 2. Выводим примеры для каждого значения (внутри этого блока)
      (($val.meanings // [] | to_entries) as $entries |
      $entries[] |
      .key as $idx |
      
      (.value.examples // [] | .[] |
        "\($pad)\(beige)\(.en)\(reset)",
        "\($pad)\(.ru)",
        ""
      ),
      
      # Разделитель между блоками (но не после последнего)
      (if $idx < ($entries | length) - 1 then "\($pad)\(white)----------\(reset)" else empty end)),

      # 3. Финальный разделитель (выводится ОДИН раз после всех примеров)
      "\(white)\($ddash)\(reset)",

      # 4. Краткий список значений (выводится ОДИН раз, так как обращаемся к $val)
      ($val.meanings // [] | to_entries[] |
        "\(beige)\(.key + 1). \(.value.definition)\(reset) \(mate)(\(.value.synonyms // [] | join(", ")))\(reset)"
      )
'
    ;;
  "tp")
    echo "preposition of time"
    path_to_file=/home/stepan/git_repos/kn7072/EnglishArticles/preposition/base_time.json
    jq_key_command=".blocks[].items[].phrase_en"
    # jq_filter='.blocks[].items[] | select(.phrase_en == "%s").examples[] | "EN: \(.en)\nRU: \(.ru)\n---"'
    # shellcheck disable=SC2016
    jq_filter='
      def cyan: "\u001b[38;2;0;255;255m";
      def bold: "\u001b[1m";
      def reset: "\u001b[0m";
      def aquamarine: "\u001b[38;2;127;255;212m";
      def powderblue: "\u001b[38;2;176;224;230m";
      def white: "\u001b[38;2;255;255;255m";
      def beige: "\u001b[38;2;245;245;220m";

      4 as $indent |
      (" " * $indent) as $pad |
      ("-" * 21) as $ddash |
      ("========" * $indent) as $start_block |


      # Ищем фразу внутри всех блоков и всех items
      .blocks[] |
      .category as $cat | 
      .items[] |
      select(.phrase_en == $word) |
      . as $val |

      "\(cyan)\($start_block)\(reset)   \($word)   \(cyan)\($start_block)\(reset)",

      # 1. Блок со всеми примерами
      ($val.examples // [] | .[] |
        "\($pad)\(beige)\(.en)\(reset)",
        "\($pad)\(.ru)",
        ""
      ),
      
      # 2. Заголовок со словом
      "\(bold)\(aquamarine)\($val.phrase_en)\(reset) - \(beige)\($val.phrase_ru)  \(powderblue)(\($cat))\(reset)"
        '
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
# command=$(printf "${jq_filter}" "${word}")

jq -r --arg word "$word" "${jq_filter}" "${path_to_file}"
# echo "${word}"
# echo "${command}"
# echo "${jq_filter}"
# set +x
