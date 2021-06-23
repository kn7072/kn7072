#!/bin/bash
export DISPLAY=:0

player_name="clementine"
pid_player=$(ps -C ${player_name} -o pid=)

if (($pid_player)); then
    echo "${player_name} уже запущена, pid=$pid_player"
    echo "Выполняем команду ${player_name} $1"
    nohup clementine $1 &
else 
    nohup clementine & 
    echo "Выполняем команду ${player_name} $1"
    nohup clementine $1 & # выполняем команду
    echo "Запустили $player_name, pid=$!"
fi 


