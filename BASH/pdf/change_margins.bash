#!/bin/bash

# сюда попадают страницы для создания документа  './for-book/' './for-test-margins'
dir_with_files_margins='./for-book'  

 # тут лежат страницы без отступов './temp-margins-0'  './for_test/'
dir_with_margin_0='./temp-margins-0/'  # './temp-margins-0-header/'  './temp-margins-0/' 


for FILE in `find ${dir_with_margin_0} -type f -name '*page.pdf' | sort -V`; do
    echo "${FILE}"
    arrIN=(${FILE//_/ })
    echo ${arrIN[0]}
    echo ${arrIN[0]//$dir_with_margin_0/}
    number_zeros=${arrIN[0]//$dir_with_margin_0/}
    number=$((10#$number_zeros))
    if [[ $(( number%2)) -eq 0 ]]; then
        echo "четное"
        path_file=${dir_with_files_margins}/${number}_m_${arrIN[1]}
        echo "${path_file}"
        # left top right bottom
        
        # для оглавления
        # pdfcrop --margins '20 45 70 45' "${FILE}" "${path_file}"

        pdfcrop --margins '70 45 20 45' "${FILE}" "${path_file}"
    else
        echo "нечетное"
        path_file=${dir_with_files_margins}/${number}_m_${arrIN[1]}
        echo "${path_file}"
        
        # для оглавления
        # pdfcrop --margins '70 45 20 45' "${FILE}" "${path_file}"

        pdfcrop --margins '20 45 70 45' "${FILE}" "${path_file}"
    fi
done
