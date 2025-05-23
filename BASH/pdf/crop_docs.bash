#!/bin/bash
dir_with_files='./temp2/'  # тут лежат файлы оригинальных страниц
dir_with_margin_0='./temp-margins-0' # сюда попадают страницы без отступов

mkdir -p "${dir_with_margin_0}"

for FILE in `find $dir_with_files -type f -name '*page.pdf' | sort -V`; do
    echo "${FILE}"
    arrIN=(${FILE//_/ })
    # echo ${arrIN[0]}
    echo ${arrIN[0]//$dir_with_files/}
    number_zeros=${arrIN[0]//$dir_with_files/}
    number=$((10#$number_zeros))
    if [[ $(( number%2)) -eq 0 ]]; then
        echo "четное"
        path_file=${dir_with_margin_0}/${number}_output_${arrIN[1]}
        echo "${path_file}"
        pdfcrop --margins '0 0 0 0' "${FILE}" "${path_file}"
    else
        echo "нечетное"
        path_file=${dir_with_margin_0}/${number}_output_${arrIN[1]}
        echo "${path_file}"
        pdfcrop --margins '0 0 0 0' "${FILE}" "${path_file}"
    fi
done
