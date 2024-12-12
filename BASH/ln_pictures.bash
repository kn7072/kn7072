#!/bin/bash
IFS=$'\n'
printf "source ${1}\ntarget ${2}\n\n"

if [[ ! (-d $1 && -d $2) ]]; then
    echo "one of '$1', '$2' in not dir"
    exit 1 
fi

# set -x
array_names=('*.jpg*' '*.jpeg*' '*.png*')
filter_names=""
for i in "${array_names[@]}"; do echo $i; filter_names+=" -name \"${i}\" -o "; done
filter_names=${filter_names::-3}
printf "filter_names '${filter_names}'\n"

find_command="find \"${1}\" -type f ${filter_names}"  # find
printf "'find_command ${find_command}'\n"


for file in $(eval ${find_command}); do #find "${1}" -type f ${filter_names}
    printf "file_name ${file}\n"
    new_name=$(echo "${file}" | awk -F"/" '{print $(NF)}' | sed "s/.*\(.\{30,50\}$\)/\1/") 
    name_for_link="${2}/$( date +%s )_${new_name}"
    printf "new_file_name ${name_for_link}\n"
    ln -s ${file} ${name_for_link}
done
# set +x
# для пояснения: : является сокращением для true и true не обрабатывает никаких параметров., Важен пробел между : и '
: '
./ln_pictures.bash ~/"картины/Alfred Sisley" ~/"картины_раб_стол"
./ln_pictures.bash ~/"картины/Живопись картины русских художников 18-20 веков jpeg-600шт" ~/"картины_раб_стол"
./ln_pictures.bash ~/"картины/Иероним БОСХ (Hieronymus Bosch) (ок.1450 - 1516)" ~/"картины_раб_стол"
./ln_pictures.bash ~/"картины/Peter Paul Rubens (1577-1640)" ~/"картины_раб_стол"
'
