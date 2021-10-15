#!/bin/bash

invalid-input () {
echo "Invalid input '$dir_name' '$count_files'" >&2
exit 1
}

create_file() {
    if [[ -e $1 ]]; then
            echo "Файл существует - $1"
        else 
            touch $1
    fi
return 0    
}

create_all_files() {
    count=1
    while [ $count -le $2 ]
    do
        file_name="$1/$count"
        file_name_eng="${file_name}_eng"
        create_file $file_name
        create_file $file_name_eng
        count=$(( $count + 1 ))
    done
    echo "This is the end of the create_all_files"
return 0
}

read -p "Введите имя каталога(число) и число файлов -> " dir_name count_files
[[ -z "$dir_name" || -z "$count_files" ]] && invalid-input

path_dir="./$dir_name"
# path_dir="$(pwd)/$dir_name"
echo $path_dir
if [[ -d path_dir ]]; then
    echo "Каталог существует $path_dir"
else
    echo "Создаем каталог $path_dir"
    mkdir $path_dir
fi

create_all_files $path_dir $count_files

