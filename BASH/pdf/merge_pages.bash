#!/bin/bash

count_pages_for_merge=50
dir_with_files="./ready_files"
path_to_output="./ready_for_print.pdf"
counter=0
files_for_merge=""

echo "start"
for FILE in $(find ${dir_with_files} -type f -name '*page.pdf' | sort -V); do

  echo "${FILE}"
  files_for_merge="${files_for_merge} ${FILE}"

  # ge больше или равно
  if [[ $counter -ge $count_pages_for_merge ]]; then
    echo "${files_for_merge}"
    counter=0
    if [[ -e "${path_to_output}" ]]; then
      # файл сущуствует - значит перепишем его с добавлением новой порции страниц
      command_merge="cpdf -merge ${path_to_output} ${files_for_merge} -o ${path_to_output}"
      echo "${command_merge}"
      eval "${command_merge}"
    else
      # создаем первую версию результирующего файла
      command_merge="cpdf -merge ${files_for_merge} -o ${path_to_output}"
      echo "${command_merge}"
      eval "${command_merge}"
    fi
    # обнуляем список страниц для новой порции
    files_for_merge=""
  else
    counter=$(bc <<<"sclale=0;${counter}+1")
  fi
done

# цикл закончился, но возможно files_for_merge еще содержит страницы которые нужно добавить
if [[ -n "${files_for_merge}" ]]; then
  # длина строки не равна нулю
  command_merge="cpdf -merge ${path_to_output} ${files_for_merge} -o ${path_to_output}"
  echo "${command_merge}"
  eval "${command_merge}"
fi
