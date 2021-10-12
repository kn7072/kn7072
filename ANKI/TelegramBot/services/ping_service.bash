#!/bin/bash

count_ping=1
template="$count_ping packets transmitted, $count_ping received, 0% packet loss"
time_sleep=60

current_requests=0

while true; do
    ping_output=$( ping -c $count_ping 8.8.8.8 )
    # echo $ping_output
    case "$ping_output" in
        *$template*);;
        *) echo "Проблемы с сетью\n $ping_output"
            sleep $time_sleep
            systemctl restart networking.service
            exit 1
            ;;
    esac
    
    # let current_requests+=1
    # echo $current_requests
    # if (($current_requests > 3)); then
    #     echo "TEST"
    #     sleep 180
    #     exit 1
    # fi    
    
    sleep $time_sleep
done