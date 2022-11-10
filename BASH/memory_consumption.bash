#!/bin/bash

process_pid=-1

if [[ $# -ne 1 ]]; then
    echo "Ожидается получить один аргимент - pid процесса"
else
    echo "pid of process is $1"
    process_pid=$1
    echo $(ps -p "$1")
fi
