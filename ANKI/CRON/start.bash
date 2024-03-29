#!/bin/bash
export DISPLAY=:0

player_name="clementine"
pid_player=$(ps -C ${player_name} -o pid=)
echo "Start PID ${pid_player}"

if (($pid_player)); then
    echo "${player_name} уже запущена, pid=$pid_player"
    echo "Выполняем команду ${player_name} $1"
    clementine $1 &
else 
    clementine & 
    echo "Выполняем команду ${player_name} $1"
    clementine $1 & # выполняем команду
    echo "Запустили $player_name, pid=$!"
fi 


