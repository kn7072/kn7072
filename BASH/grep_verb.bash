#!/bin/bash

path_to_file="./список_глаголов_из_голицына.txt"
start_message="Введите фразу для поиска:"
# set -x
echo -n "$start_message"
while true; do
    read input
    
    if [[ "$input" ]]; then
        grep -iE --color ${input} ${path_to_file}
        if [[ ${input} == "exit" ]]; then
            break
        fi
        echo ""
    else
        echo -n "$start_message"
    fi
done

# set +x
exit
