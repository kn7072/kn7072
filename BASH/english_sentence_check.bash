#!/bin/bash

start_xclip="start"
start_clipboard="clipboard_" # буфер ctrl + c
service_url="http://192.168.1.53:8088"
service_url="http://localhost:8090"
temp_file_name="stdout"

while true; do
    primery_clip=$(xclip -o -selection primery)
    clipboard=$(xclip -o -selection clipboard) # буфер ctrl + c
    
    if [[ "${primery_clip}" == "${start_xclip}" ]]; then
        if [[ "${clipboard}" != "${start_clipboard}" ]]; then
            start_clipboard=$clipboard
            clear
            request=$(curl -s -X POST -F "word=${primery_clip}" ${service_url}/word_all_examples)
            printf "$request\n"
            echo "$request\n" > $temp_file_name
        fi
        sleep 2
    else
        # printf "start start_xclip ${start_xclip}\n"
        # printf "start primery_clip ${primery_clip}\n"
        
        start_xclip=$primery_clip
        # printf "${primery_clip}\n"
        clear
        request=$(curl -s -X POST -F "word=${primery_clip}" ${service_url}/word)
        printf "$request\n"
        echo "$request\n" > $temp_file_name
        # printf "end start_xclip ${start_xclip}\n"

	    # озвучиваем слово
        request=$(curl -s -X POST -F "word=${primery_clip}" ${service_url}/sound)
        # printf "end primery_clip ${primery_clip}\n"
        # printf "########################\n"
        # sleep 15
    fi
done

