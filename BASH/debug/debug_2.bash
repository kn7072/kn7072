#!/bin/bash
# https://habr.com/ru/post/666982/

function _debug_for_bash() {
    echo "# $BASH_COMMAND"
    while read -p "debug> " _cmnd; do
        if [ -n "$_cmnd" ]; then
            eval "$_cmnd"
        else
            break
        fi
    done
}

trap '_debug_for_bash' DEBUG

echo "$PATH"
echo $((2 + 3))
